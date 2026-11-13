# -*- coding: utf-8 -*-
"""Analise de Gap Regulatorio — BooX Fase 1.

Compara os TESTES CANONICOS aplicaveis ao tipo de instituicao com o que
o banco executa (B_TESTES_execucao) e os controles que enderecam (B5).

Uso:
    python -m boox.gap_regulatorio <pasta_instancia> [--tipo <tipo>] [--out <arquivo.md>]
"""
import csv, os, sys
from collections import defaultdict

def _ler(c):
    if not os.path.exists(c): return []
    with open(c, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))

def _preenchido(v): return v is not None and str(v).strip() != ""

def _canonico_dir(pasta):
    for cand in [os.path.join(pasta,"..","..","canonico"),
                 os.path.join(os.path.dirname(__file__),"..","canonico")]:
        if os.path.isdir(cand): return cand
    return None

def analisar(pasta, tipo_instituicao=None):
    canon = _canonico_dir(pasta)
    if not canon: return {"erro":"Camada canonica nao encontrada"}
    testes = _ler(os.path.join(canon,"B_TESTES_canonico.csv"))
    fr = _ler(os.path.join(canon,"B_FR_canonico.csv"))
    execs = _ler(os.path.join(pasta,"B_TESTES_execucao.csv"))
    controles = _ler(os.path.join(pasta,"B5_controles.csv"))

    aplicaveis=[]
    for t in testes:
        if t.get("status") not in ("ativo","proposto"): continue
        if tipo_instituicao:
            ap = t.get("aplicabilidade","").strip()
            if ap and tipo_instituicao not in ap.split("|"): continue
        aplicaveis.append(t)

    exec_por_t=defaultdict(list)
    for e in execs:
        exec_por_t[e.get("teste_canonico_id","")].append(e)

    resultados=[]
    for t in aplicaveis:
        tid=t["id"]; lst=exec_por_t.get(tid,[])
        if not lst:
            estado="sem_execucao"; res=None; cid=None
        else:
            e=sorted(lst,key=lambda x:x.get("data_ultimo",""),reverse=True)[0]
            res=e.get("resultado_ultimo","nao_executado"); cid=e.get("controle_id","")
            if res=="conforme": estado="atendido"
            elif res=="parcialmente_conforme": estado="parcial"
            elif res=="nao_conforme": estado="nao_conforme"
            elif res=="na": estado="nao_aplicavel_declarado"
            else: estado="sem_execucao"
        resultados.append({
            "teste_id":tid,"regulador":t.get("regulador",""),"norma_id":t.get("norma_id",""),
            "titulo":t.get("titulo",""),"criticidade":t.get("criticidade","media"),
            "risco_r0":t.get("risco_r0_canonico",""),"fator_risco":t.get("fator_risco_canonico_id",""),
            "controle_esperado":t.get("controle_esperado_texto",""),
            "estado":estado,"resultado":res,"controle_id_real":cid,
        })

    gaps_criticos=[r for r in resultados if r["criticidade"]=="alta"
                   and r["estado"] not in ("atendido","nao_aplicavel_declarado")]

    por_reg=defaultdict(lambda:{"total":0,"atendido":0,"parcial":0,"nao_conforme":0,"sem_execucao":0,"na":0})
    for r in resultados:
        reg=r["regulador"] or "?"
        por_reg[reg]["total"]+=1
        if r["estado"]=="atendido": por_reg[reg]["atendido"]+=1
        elif r["estado"]=="parcial": por_reg[reg]["parcial"]+=1
        elif r["estado"]=="nao_conforme": por_reg[reg]["nao_conforme"]+=1
        elif r["estado"]=="nao_aplicavel_declarado": por_reg[reg]["na"]+=1
        else: por_reg[reg]["sem_execucao"]+=1

    ctrl_em_exec={e.get("controle_id","") for e in execs if _preenchido(e.get("controle_id"))}
    orfaos=[c for c in controles if c["id"] not in ctrl_em_exec]

    fr_status=defaultdict(lambda:{"total_testes":0,"testes_atendidos":0})
    for r in resultados:
        f=r.get("fator_risco","")
        if not f: continue
        fr_status[f]["total_testes"]+=1
        if r["estado"]=="atendido": fr_status[f]["testes_atendidos"]+=1
    fr_descob=[(k,v) for k,v in fr_status.items() if v["testes_atendidos"]==0]

    return {
        "tipo_instituicao":tipo_instituicao,
        "testes_aplicaveis":len(aplicaveis),
        "testes_avaliados":resultados,
        "cobertura_por_regulador":dict(por_reg),
        "gaps_criticos":gaps_criticos,
        "controles_orfaos":orfaos,
        "fatores_risco_descobertos":fr_descob,
    }

def render_md(rel, caminho):
    L=["# Analise de Gap Regulatorio — BooX",""]
    if rel.get("erro"):
        L.append(f"**ERRO:** {rel['erro']}")
        open(caminho,"w",encoding="utf-8").write("\n".join(L)); return
    tipo=rel.get("tipo_instituicao") or "(todos os tipos)"
    L.append(f"Tipo de instituicao: **{tipo}**")
    L.append(f"Testes canonicos aplicaveis: **{rel['testes_aplicaveis']}**"); L.append("")
    L.append("## Cobertura por regulador"); L.append("")
    L.append("| Regulador | Total | Atendido | Parcial | Nao conforme | Sem execucao | N/A |")
    L.append("|-----------|-------|----------|---------|--------------|--------------|-----|")
    for reg,s in sorted(rel["cobertura_por_regulador"].items()):
        pct=round(100*s["atendido"]/s["total"],1) if s["total"] else 0
        L.append(f"| **{reg}** | {s['total']} | {s['atendido']} ({pct}%) | {s['parcial']} | {s['nao_conforme']} | {s['sem_execucao']} | {s['na']} |")
    L.append("")
    gc=rel["gaps_criticos"]
    L.append(f"## Gaps criticos (alta criticidade sem atendimento): **{len(gc)}**"); L.append("")
    if gc:
        for r in gc[:30]:
            L.append(f"- **[{r['regulador']}]** {r['teste_id']} — {r['titulo']} (estado: {r['estado']})")
    else:
        L.append("Nenhum gap critico identificado.")
    L.append("")
    orf=rel["controles_orfaos"]
    L.append(f"## Controles orfaos (sem teste canonico associado): **{len(orf)}**"); L.append("")
    L.append("Podem ser controles especificos do banco (legitimos) ou trabalho sem sustentacao regulatoria. Vale revisar.")
    if orf:
        L.append("")
        for c in orf[:15]:
            L.append(f"- {c['id']} — {c.get('acao','')[:70]}")
    L.append("")
    fd=rel["fatores_risco_descobertos"]
    L.append(f"## Fatores de Risco descobertos: **{len(fd)}**"); L.append("")
    L.append("FRs canonicos cujos testes NAO estao atendidos — sinal de vulnerabilidade."); L.append("")
    for f,s in fd:
        L.append(f"- {f} (testes: {s['total_testes']} · atendidos: {s['testes_atendidos']})")
    L.append("")
    L.append("---"); L.append("_Gerado pela engine de gap regulatorio do BooX._")
    open(caminho,"w",encoding="utf-8").write("\n".join(L))

def main():
    if len(sys.argv)<2:
        print(__doc__); sys.exit(0)
    pasta=sys.argv[1]
    tipo=None
    if "--tipo" in sys.argv: tipo=sys.argv[sys.argv.index("--tipo")+1]
    saida=os.path.join(pasta,"gap_regulatorio.md")
    if "--out" in sys.argv: saida=sys.argv[sys.argv.index("--out")+1]
    rel=analisar(pasta,tipo_instituicao=tipo)
    render_md(rel,saida)
    if rel.get("erro"):
        print("ERRO:",rel["erro"]); sys.exit(1)
    print(f"Gap regulatorio gerado em: {saida}")
    print(f"  Testes aplicaveis: {rel['testes_aplicaveis']}")
    print(f"  Gaps criticos: {len(rel['gaps_criticos'])}")
    print(f"  Controles orfaos: {len(rel['controles_orfaos'])}")
    print(f"  Fatores descobertos: {len(rel['fatores_risco_descobertos'])}")

if __name__=="__main__": main()
