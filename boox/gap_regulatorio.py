# -*- coding: utf-8 -*-
"""Analise de Gap Regulatorio — BooX Fase 1.

Compara os TESTES CANONICOS aplicaveis ao tipo de instituicao com o que
o banco executa (B_TESTES_execucao) e os controles que enderecam (B5).

Introduz duas analises complementares:

  1. Requisitos regulatorios nao atendidos — TODOS os testes aplicaveis
     que nao estao em estado 'atendido' (independente de criticidade).
     Agrupados por estado (parcial / nao_conforme / sem_execucao).

  2. Controles internos (nao regulatorios) — controles do B5 sem teste
     canonico especifico mapeado. Aplicamos inferencia por moldura: se
     o controle visa risco operacional, conformidade, cyber, PLD ou
     privacidade, ele atende a norma-moldura correspondente (CMN 4.557
     etc.) mesmo sem teste pontual. Controles sem nenhuma moldura
     inferida ficam como 'sem_moldura' — candidatos a revisao.

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

# ---------------------------------------------------------------------------
# Regra de inferencia por moldura regulatoria
# ---------------------------------------------------------------------------
# Dado o risco R0 canonico que um controle visa (resolvido via B_MAP),
# retorna a norma-moldura mais ampla que esse controle automaticamente
# atende, mesmo sem teste pontual mapeado.
MOLDURA_POR_R0 = {
    "R0.U.1":  ("CMN 4.557", "Gerenciamento de risco de credito"),
    "R0.U.2":  ("CMN 4.557", "Gerenciamento de risco de mercado"),
    "R0.U.3":  ("CMN 4.557", "Gerenciamento de risco de liquidez"),
    "R0.U.4":  ("CMN 4.557", "Gerenciamento de risco de taxa de juros (IRRBB)"),
    "R0.U.5":  ("CMN 4.557", "Gerenciamento de risco de variacao cambial"),
    "R0.U.6":  ("CMN 4.557", "Gerenciamento de risco operacional"),
    "R0.U.7":  ("CMN 4.893", "Politica de seguranca cibernetica"),
    "R0.U.8":  ("CMN 4.557", "Gerenciamento de risco de modelo"),
    "R0.U.9":  ("CMN 4.557", "Gerenciamento de resiliencia operacional"),
    "R0.U.10": ("CMN 4.557", "Gerenciamento de risco de fornecedores e terceiros"),
    "R0.U.11": ("CMN 4.557", "Gerenciamento de risco de conformidade"),
    "R0.U.12": ("CMN 4.860", "Gestao de ouvidoria e conduta"),
    "R0.U.13": ("Lei 9.613", "Prevencao a lavagem de dinheiro e FT"),
    "R0.U.14": ("LGPD (Lei 13.709)", "Protecao de dados pessoais"),
}

def _moldura_para_r0(r0):
    """Resolve R0 ou qualquer subnivel R1-R4 para a mesma moldura do R0."""
    if not r0: return None
    r0_raiz = ".".join(r0.split(".")[:3]) if r0.count(".") >= 2 else r0
    return MOLDURA_POR_R0.get(r0_raiz)

def analisar(pasta, tipo_instituicao=None):
    canon = _canonico_dir(pasta)
    if not canon: return {"erro":"Camada canonica nao encontrada"}
    testes = _ler(os.path.join(canon,"B_TESTES_canonico.csv"))
    fr = _ler(os.path.join(canon,"B_FR_canonico.csv"))
    riscos_canon = _ler(os.path.join(canon,"B6_riscos_canonico.csv"))
    execs = _ler(os.path.join(pasta,"B_TESTES_execucao.csv"))
    controles = _ler(os.path.join(pasta,"B5_controles.csv"))
    bmap = _ler(os.path.join(pasta,"B_MAP_taxonomia.csv"))

    # de-para risco local -> canonico
    canon_by_local = {m["termo_local_id"]: m["canonico_id"]
                      for m in bmap if m.get("dominio") == "risco"
                      and m.get("status") in ("aprovado", "ajustado")}

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

    # --- gaps criticos (compat: criticidade alta sem atendimento) ---
    gaps_criticos=[r for r in resultados if r["criticidade"]=="alta"
                   and r["estado"] not in ("atendido","nao_aplicavel_declarado")]

    # --- requisitos nao atendidos (TODOS, por criticidade) ---
    nao_atendidos = [r for r in resultados if r["estado"] not in ("atendido","nao_aplicavel_declarado")]
    nao_atendidos_por_crit = {"alta": [], "media": [], "baixa": []}
    for r in nao_atendidos:
        nao_atendidos_por_crit.setdefault(r["criticidade"], []).append(r)

    # --- cobertura por regulador ---
    por_reg=defaultdict(lambda:{"total":0,"atendido":0,"parcial":0,"nao_conforme":0,"sem_execucao":0,"na":0})
    for r in resultados:
        reg=r["regulador"] or "?"
        por_reg[reg]["total"]+=1
        if r["estado"]=="atendido": por_reg[reg]["atendido"]+=1
        elif r["estado"]=="parcial": por_reg[reg]["parcial"]+=1
        elif r["estado"]=="nao_conforme": por_reg[reg]["nao_conforme"]+=1
        elif r["estado"]=="nao_aplicavel_declarado": por_reg[reg]["na"]+=1
        else: por_reg[reg]["sem_execucao"]+=1

    # --- controles internos (nao regulatorios) + inferencia por moldura ---
    ctrl_em_exec={e.get("controle_id","") for e in execs if _preenchido(e.get("controle_id"))}
    nao_mapeados = [c for c in controles if c["id"] not in ctrl_em_exec]

    internos_classificados = []
    for c in nao_mapeados:
        risco_local = c.get("risco_id","")
        r0 = canon_by_local.get(risco_local, "")
        moldura = _moldura_para_r0(r0)
        internos_classificados.append({
            "id": c["id"],
            "acao": c.get("acao",""),
            "risco_local": risco_local,
            "risco_r0_canonico": r0,
            "moldura_norma": moldura[0] if moldura else "",
            "moldura_descricao": moldura[1] if moldura else "",
            "classificacao": "atende_moldura" if moldura else "sem_moldura",
        })
    atendem_moldura = [c for c in internos_classificados if c["classificacao"]=="atende_moldura"]
    sem_moldura     = [c for c in internos_classificados if c["classificacao"]=="sem_moldura"]

    # agregado de molduras inferidas
    por_moldura = defaultdict(int)
    for c in atendem_moldura:
        por_moldura[c["moldura_norma"]] += 1

    # --- fatores de risco descobertos ---
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
        "requisitos_nao_atendidos":nao_atendidos,
        "requisitos_nao_atendidos_por_criticidade":nao_atendidos_por_crit,
        "controles_internos_nao_mapeados":internos_classificados,
        "controles_internos_atendem_moldura":atendem_moldura,
        "controles_internos_sem_moldura":sem_moldura,
        "molduras_inferidas":dict(por_moldura),
        # compat retroativa
        "controles_orfaos":nao_mapeados,
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

    na = rel["requisitos_nao_atendidos"]
    L.append(f"## Requisitos regulatorios nao atendidos — **{len(na)}**")
    L.append("")
    L.append("Testes canonicos aplicaveis que NAO estao em estado 'atendido'. Inclui parcial, nao conforme e sem execucao.")
    L.append("")
    por_c = rel["requisitos_nao_atendidos_por_criticidade"]
    for crit in ["alta","media","baixa"]:
        if por_c.get(crit):
            L.append(f"### Criticidade {crit} — {len(por_c[crit])}")
            for r in por_c[crit][:30]:
                L.append(f"- **[{r['regulador']}]** {r['teste_id']} — {r['titulo']} (estado: {r['estado']})")
            L.append("")

    im = rel["controles_internos_nao_mapeados"]
    am = rel["controles_internos_atendem_moldura"]
    sm = rel["controles_internos_sem_moldura"]
    L.append(f"## Controles internos (nao regulatorios) — **{len(im)}**")
    L.append("")
    L.append("Controles do banco (B5) sem teste canonico especifico mapeado. Analise por moldura:")
    L.append(f"- **{len(am)}** atendem norma-moldura (ex: CMN 4.557 para risco operacional) — legitimos, mas sem teste pontual mapeado")
    L.append(f"- **{len(sm)}** sem moldura inferida — candidatos a revisao")
    L.append("")
    if rel["molduras_inferidas"]:
        L.append("### Agregado por moldura inferida")
        L.append("")
        L.append("| Moldura | Qtd controles |")
        L.append("|---------|---------------|")
        for norma, qtd in sorted(rel["molduras_inferidas"].items(), key=lambda x: -x[1]):
            L.append(f"| **{norma}** | {qtd} |")
        L.append("")
    if am:
        L.append("### Controles que atendem moldura (amostra)")
        for c in am[:15]:
            L.append(f"- {c['id']} ({c['moldura_norma']}) — {c['acao'][:70]}")
        L.append("")
    if sm:
        L.append("### Controles sem moldura identificada")
        for c in sm[:15]:
            L.append(f"- {c['id']} — {c['acao'][:70]}")
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
    print(f"  Requisitos nao atendidos: {len(rel['requisitos_nao_atendidos'])}")
    print(f"  Gaps criticos (alta): {len(rel['gaps_criticos'])}")
    print(f"  Controles internos (nao regulatorios): {len(rel['controles_internos_nao_mapeados'])}")
    print(f"    - atendem moldura: {len(rel['controles_internos_atendem_moldura'])}")
    print(f"    - sem moldura: {len(rel['controles_internos_sem_moldura'])}")
    print(f"  Fatores descobertos: {len(rel['fatores_risco_descobertos'])}")

if __name__=="__main__": main()
