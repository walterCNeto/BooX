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
import csv, os, sys, datetime
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
    "R0.U.12": ("CMN 4.860", "Gestao de ouvidoria e conduta"),  # distribuidores: ver _moldura_para_r0
    "R0.U.13": ("Circ. BCB 3.978", "Prevencao a lavagem de dinheiro e FT (PLD-FT)"),
    "R0.U.14": ("LGPD (Lei 13.709)", "Protecao de dados pessoais"),
}

# Tipos fora do escopo da CMN 4.893 (art. 1, par. unico, Res. CMN 5.117/2024).
TIPOS_FORA_CMN_4893 = {"corretora", "dtvm", "distribuidora", "consorcio", "instituicao_pagamento"}
# Tipos que distribuem produtos (suitability: Res. CVM 30 + ANBIMA).
TIPOS_DISTRIBUIDORES = {"corretora", "dtvm", "distribuidora", "banco_multiplo", "banco_comercial"}
# Tipos fora do escopo da Circ. BCB 3.978 (ver CHANGELOG 1.4.0).
TIPOS_FORA_CIRC_3978 = {"seguradora", "previdencia", "capitalizacao",
                        "administrador_fiduciario", "gestor_recursos"}

def _moldura_para_r0(r0, tipo=None):
    """Resolve R0 ou qualquer subnivel R1-R4 para a moldura do R0, ajustada ao tipo."""
    if not r0: return None
    r0_raiz = ".".join(r0.split(".")[:3]) if r0.count(".") >= 2 else r0
    if r0_raiz == "R0.U.7" and tipo in TIPOS_FORA_CMN_4893:
        return ("Res. CVM 35 art. 45", "Seguranca cibernetica (CMN 4.893 nao se aplica ao tipo)")
    if r0_raiz == "R0.U.12" and tipo in TIPOS_DISTRIBUIDORES:
        return ("Res. CVM 30 + ANBIMA Suitability", "Suitability e conduta na distribuicao")
    if r0_raiz == "R0.U.13" and tipo in TIPOS_FORA_CIRC_3978:
        return ("Lei 9.613", "Prevencao a lavagem de dinheiro e FT (Circ. BCB 3.978 nao se aplica ao tipo)")
    return MOLDURA_POR_R0.get(r0_raiz)

def _fora_de_vigencia(t, hoje):
    vi = t.get("vigencia_inicio", "").strip(); vf = t.get("vigencia_fim", "").strip()
    if vf and vf < hoje: return f"vigencia encerrada em {vf}"
    if vi and vi > hoje: return f"vigencia inicia em {vi}"
    return None

def _grupos_equivalencia(testes):
    """Union-find sobre equivale_a: id -> raiz (menor id) do grupo."""
    pai = {t["id"]: t["id"] for t in testes}
    def raiz(x):
        while pai[x] != x:
            pai[x] = pai[pai[x]]; x = pai[x]
        return x
    for t in testes:
        eq = t.get("equivale_a", "").strip()
        if eq and eq in pai:
            a, b = raiz(t["id"]), raiz(eq)
            if a != b: pai[max(a, b)] = min(a, b)
    return {i: raiz(i) for i in pai}

def analisar(pasta, tipo_instituicao=None, hoje=None):
    hoje = hoje or datetime.date.today().isoformat()
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

    grupo = _grupos_equivalencia(testes)

    candidatos=[]; fora_vigencia=[]; excluidos_por_norma=defaultdict(int)
    for t in testes:
        if t.get("status") not in ("ativo","proposto"): continue
        if tipo_instituicao:
            ap = t.get("aplicabilidade","").strip()
            if ap and tipo_instituicao not in ap.split("|"):
                excluidos_por_norma[t.get("norma_id","") or "?"] += 1
                continue
        motivo = _fora_de_vigencia(t, hoje)
        if motivo:
            fora_vigencia.append({"teste_id":t["id"],"norma_id":t.get("norma_id",""),
                                  "titulo":t.get("titulo",""),"motivo":motivo,
                                  "revogada_por":t.get("revogada_por","")})
            continue
        candidatos.append(t)

    # equivale_a: um unico representante (menor id) por grupo
    por_grupo = defaultdict(list)
    for t in candidatos: por_grupo[grupo[t["id"]]].append(t)
    aplicaveis=[]; equivalentes_agrupados=[]
    for lst_g in por_grupo.values():
        lst_g.sort(key=lambda x: x["id"])
        aplicaveis.append(lst_g[0])
        if len(lst_g) > 1:
            equivalentes_agrupados.append({"representante":lst_g[0]["id"],
                                           "equivalentes":[x["id"] for x in lst_g[1:]]})
    aplicaveis.sort(key=lambda x: x["id"])
    rep_do_grupo = {g: lst_g[0]["id"] for g, lst_g in por_grupo.items()}
    norma_aplicavel = {t.get("norma_id","") or "?" for t in aplicaveis}
    normas_excluidas = [{"norma_id":n,"testes_excluidos":q,"totalmente_excluida":n not in norma_aplicavel}
                        for n, q in sorted(excluidos_por_norma.items())]

    exec_por_t=defaultdict(list)
    for e in execs:
        tid_e = e.get("teste_canonico_id","")
        # execucao de qualquer teste equivalente vale para o representante do grupo
        alvo = rep_do_grupo.get(grupo.get(tid_e), tid_e)
        exec_por_t[alvo].append(e)

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
            "status_teste":t.get("status",""),
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

    # --- proposto x ativo (validado) ---
    por_status={s:{"total":0,"atendido":0,"parcial":0,"nao_conforme":0,"sem_execucao":0,"na":0}
                for s in ("ativo","proposto")}
    chave_estado={"atendido":"atendido","parcial":"parcial","nao_conforme":"nao_conforme",
                  "nao_aplicavel_declarado":"na"}
    for r in resultados:
        b=por_status[r["status_teste"]]; b["total"]+=1
        b[chave_estado.get(r["estado"],"sem_execucao")]+=1
    pct_validado=round(100*por_status["ativo"]["total"]/len(resultados),1) if resultados else 0.0

    # --- controles internos (nao regulatorios) + inferencia por moldura ---
    ctrl_em_exec={e.get("controle_id","") for e in execs if _preenchido(e.get("controle_id"))}
    nao_mapeados = [c for c in controles if c["id"] not in ctrl_em_exec]

    internos_classificados = []
    for c in nao_mapeados:
        risco_local = c.get("risco_id","")
        r0 = canon_by_local.get(risco_local, "")
        moldura = _moldura_para_r0(r0, tipo_instituicao)
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
        "data_referencia":hoje,
        "testes_aplicaveis":len(aplicaveis),
        "cobertura_por_status":por_status,
        "pct_validado":pct_validado,
        "testes_fora_vigencia":fora_vigencia,
        "equivalentes_agrupados":equivalentes_agrupados,
        "normas_excluidas":normas_excluidas,
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
    L.append(f"Testes canonicos aplicaveis: **{rel['testes_aplicaveis']}** (data de referencia: {rel['data_referencia']})")
    if rel.get("segmento"):
        L.append(f"Segmento (informativo, nao altera a analise): **{rel['segmento']}**")
    L.append("")
    L.append("> O BooX mede cobertura, nao prova conformidade.")
    L.append("")
    ps=rel["cobertura_por_status"]
    L.append("## Status do teste: ativo (validado) x proposto"); L.append("")
    L.append(f"Percentual validado (ativos / aplicaveis): **{rel['pct_validado']}%**"); L.append("")
    L.append("| Status | Total | Atendido | Parcial | Nao conforme | Sem execucao | N/A |")
    L.append("|--------|-------|----------|---------|--------------|--------------|-----|")
    for st in ("ativo","proposto"):
        s=ps[st]
        pct=round(100*s["atendido"]/s["total"],1) if s["total"] else 0
        L.append(f"| **{st}** | {s['total']} | {s['atendido']} ({pct}%) | {s['parcial']} | {s['nao_conforme']} | {s['sem_execucao']} | {s['na']} |")
    L.append("")
    L.append("Testes `proposto` sao sementes ainda nao validados: atende-los nao prova conformidade.")
    L.append("")
    if rel["equivalentes_agrupados"]:
        n=sum(len(g["equivalentes"]) for g in rel["equivalentes_agrupados"])
        L.append(f"Testes equivalentes (`equivale_a`) contados uma vez: {n} deduplicado(s) em {len(rel['equivalentes_agrupados'])} grupo(s).")
        L.append("")

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
    fv=rel["testes_fora_vigencia"]
    L.append(f"## Fora de vigencia — **{len(fv)}**"); L.append("")
    L.append(f"Testes nao contados: vigencia_fim anterior a {rel['data_referencia']} ou vigencia_inicio futura.")
    L.append("")
    for x in fv:
        rv=f" · revogada por {x['revogada_por']}" if x["revogada_por"] else ""
        L.append(f"- {x['teste_id']} ({x['norma_id']}) — {x['titulo']} [{x['motivo']}{rv}]")
    if not fv: L.append("_Nenhum._")
    L.append("")
    ne=rel["normas_excluidas"]
    L.append(f"## Normas excluidas para o tipo de instituicao — **{len(ne)}**"); L.append("")
    L.append("Normas com testes cuja aplicabilidade nao inclui o tipo informado (nao contados).")
    L.append("")
    for x in ne:
        tot=" (norma inteira)" if x["totalmente_excluida"] else " (parcial)"
        L.append(f"- {x['norma_id']} — {x['testes_excluidos']} teste(s){tot}")
    if not ne: L.append("_Nenhuma._")
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
    if "--segmento" in sys.argv: rel["segmento"]=sys.argv[sys.argv.index("--segmento")+1]
    render_md(rel,saida)
    if rel.get("erro"):
        print("ERRO:",rel["erro"]); sys.exit(1)
    print(f"Gap regulatorio gerado em: {saida}")
    print(f"  Testes aplicaveis: {rel['testes_aplicaveis']} (validados/ativos: {rel['pct_validado']}%)")
    print(f"  Fora de vigencia: {len(rel['testes_fora_vigencia'])}  |  Normas excluidas: {len(rel['normas_excluidas'])}")
    print(f"  Requisitos nao atendidos: {len(rel['requisitos_nao_atendidos'])}")
    print(f"  Gaps criticos (alta): {len(rel['gaps_criticos'])}")
    print(f"  Controles internos (nao regulatorios): {len(rel['controles_internos_nao_mapeados'])}")
    print(f"    - atendem moldura: {len(rel['controles_internos_atendem_moldura'])}")
    print(f"    - sem moldura: {len(rel['controles_internos_sem_moldura'])}")
    print(f"  Fatores descobertos: {len(rel['fatores_risco_descobertos'])}")

if __name__=="__main__": main()
