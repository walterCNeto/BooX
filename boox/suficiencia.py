# -*- coding: utf-8 -*-
"""Analise de suficiencia — diagnostica se os Books preenchidos bastam para avaliar."""
import csv, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "schema"))
import campos as _campos

def _ler(caminho):
    if not os.path.exists(caminho): return None
    with open(caminho, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))

def _preenchido(v): return v is not None and str(v).strip() != ""

def analisar(pasta):
    """Retorna dict com diagnostico por book + alertas estruturais."""
    rel = {"books": [], "alertas": [], "resumo": {}}
    total_obr_ok = total_obr = 0
    for nome, spec in _campos.BOOKS.items():
        linhas = _ler(os.path.join(pasta, f"{nome}.csv"))
        info = {"book": nome, "titulo": spec["titulo"], "presente": linhas is not None,
                "registros": len(linhas) if linhas else 0, "campos": []}
        if not linhas:
            info["status"] = "ausente"
            # so alerta se o book tem algum campo obrigatorio (ie e essencial)
            rel["books"].append(info); continue
        cats = {"OBR":[], "REC":[], "OPC":[]}
        for cnome, cat, tipo, dica in spec["campos"]:
            preench = sum(1 for r in linhas if _preenchido(r.get(cnome)))
            pct = round(100*preench/len(linhas)) if linhas else 0
            cats[cat].append((cnome, pct))
            if cat == "OBR":
                total_obr += 1
                if pct == 100: total_obr_ok += 1
        info["campos"] = cats
        # status do book
        obr_pcts = [p for _,p in cats["OBR"]]
        rec_pcts = [p for _,p in cats["REC"]]
        min_obr = min(obr_pcts) if obr_pcts else 100
        med_rec = round(sum(rec_pcts)/len(rec_pcts)) if rec_pcts else 100
        if min_obr == 100 and med_rec >= 70: info["status"] = "completo"
        elif min_obr == 100: info["status"] = "valido_baixa_confianca"
        else: info["status"] = "incompleto"
        info["preenchimento_obrigatorio_min"] = min_obr
        info["preenchimento_recomendado_medio"] = med_rec
        rel["books"].append(info)

    # ---- alertas estruturais cruzados ----
    proc = _ler(os.path.join(pasta,"B1_processos.csv")) or []
    risc = _ler(os.path.join(pasta,"B6_riscos.csv")) or []
    vinc = _ler(os.path.join(pasta,"B6_vinculo_processo_risco.csv")) or []
    ctrl = _ler(os.path.join(pasta,"B5_controles.csv")) or []
    serie = _ler(os.path.join(pasta,"B10_indicador_serie.csv")) or []
    kris = _ler(os.path.join(pasta,"B10_indicadores.csv")) or []
    bmap = _ler(os.path.join(pasta,"B_MAP_taxonomia.csv")) or []

    pids = {p["id"] for p in proc}
    rids = {r["id"] for r in risc}
    # hierarquia de processos
    orf = [p["id"] for p in proc if _preenchido(p.get("parent_id")) and p["parent_id"] not in pids]
    if orf: rel["alertas"].append(("processo","parent_id aponta para processo inexistente: "+", ".join(orf[:5])))
    # vinculos referenciando ids validos
    vp = [v for v in vinc if v.get("processo_id") not in pids]
    vr = [v for v in vinc if v.get("risco_id") not in rids]
    if vp: rel["alertas"].append(("vinculo",f"{len(vp)} vinculo(s) com processo_id inexistente"))
    if vr: rel["alertas"].append(("vinculo",f"{len(vr)} vinculo(s) com risco_id inexistente"))
    # riscos mapeados ao canonico
    mapeados = {m["termo_local_id"] for m in bmap if m.get("dominio")=="risco" and m.get("status") in ("aprovado","ajustado")}
    nao_map = [r["id"] for r in risc if r["id"] not in mapeados]
    if nao_map: rel["alertas"].append(("de-para",f"{len(nao_map)} risco(s) sem mapeamento canonico aprovado: "+", ".join(nao_map[:5])))
    # pares sem controle
    pares_com_ctrl = {(c.get("processo_id"),c.get("risco_id")) for c in ctrl}
    sem_ctrl = [(v["processo_id"],v["risco_id"]) for v in vinc if (v["processo_id"],v["risco_id"]) not in pares_com_ctrl]
    if sem_ctrl: rel["alertas"].append(("controle",f"{len(sem_ctrl)} par(es) processo x risco sem controle declarado (entram com penalidade)"))
    # 5W2H incompleto
    w5={"acao":"What","risco_id":"Why","responsavel":"Who","local":"Where","frequencia":"When","mecanismo":"How","cobertura_pct":"HowMuch"}
    inc=0
    for c in ctrl:
        faltam=[w for k,w in w5.items() if not _preenchido(c.get(k))]
        if faltam: inc+=1
    if inc: rel["alertas"].append(("5W2H",f"{inc} controle(s) com 5W2H incompleto (descricao parcial)"))
    # series curtas
    cont={}
    for s in serie: cont[s["indicador_id"]]=cont.get(s["indicador_id"],0)+1
    curtas=[k for k,n in cont.items() if n<3]
    sem_serie=[k["id"] for k in kris if k["id"] not in cont]
    if curtas: rel["alertas"].append(("KRI",f"{len(curtas)} KRI(s) com menos de 3 meses de serie (tendencia nao calculavel)"))
    if sem_serie: rel["alertas"].append(("KRI",f"{len(sem_serie)} KRI(s) sem serie temporal"))

    rel["resumo"]={"obrigatorios_completos":total_obr_ok,"obrigatorios_total":total_obr,
                   "books_presentes":sum(1 for b in rel["books"] if b["presente"]),
                   "books_total":len(_campos.BOOKS)}
    return rel

def render_md(rel, caminho):
    L=["# Analise de Suficiencia — BooX",""]
    r=rel["resumo"]
    L.append(f"Books presentes: **{r['books_presentes']}/{r['books_total']}** · "
             f"Campos obrigatorios 100% preenchidos: **{r['obrigatorios_completos']}/{r['obrigatorios_total']}**")
    L.append("")
    L.append("## Diagnostico por Book")
    L.append("")
    L.append("| Book | Registros | Status | Obrig. (min %) | Recom. (med %) |")
    L.append("|------|-----------|--------|----------------|----------------|")
    emoji={"completo":"OK","valido_baixa_confianca":"ATENCAO","incompleto":"FALHA","ausente":"AUSENTE"}
    for b in rel["books"]:
        if not b["presente"]:
            L.append(f"| {b['titulo']} | 0 | AUSENTE | - | - |"); continue
        L.append(f"| {b['titulo']} | {b['registros']} | {emoji.get(b['status'],b['status'])} | "
                 f"{b.get('preenchimento_obrigatorio_min','-')} | {b.get('preenchimento_recomendado_medio','-')} |")
    L.append("")
    if rel["alertas"]:
        L.append("## Alertas")
        L.append("")
        for tipo,msg in rel["alertas"]:
            L.append(f"- **[{tipo}]** {msg}")
        L.append("")
    else:
        L.append("Nenhum alerta estrutural. ")
        L.append("")
    L.append("## Legenda de status")
    L.append("")
    L.append("- **OK (completo)**: obrigatorios 100% e recomendados >= 70%. Avaliacao de alta confianca.")
    L.append("- **ATENCAO (valido, baixa confianca)**: obrigatorios 100%, mas recomendados escassos. Avalia, mas confie menos.")
    L.append("- **FALHA (incompleto)**: falta campo obrigatorio. Registros afetados nao entram no 20-box.")
    L.append("- **AUSENTE**: book nao fornecido.")
    with open(caminho,"w",encoding="utf-8") as f: f.write("\n".join(L))
