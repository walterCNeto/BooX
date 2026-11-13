# -*- coding: utf-8 -*-
"""BooX — Interface Streamlit (demonstracao publica).

Esta e a camada de apresentacao do BooX. Toda a logica de dominio vive em
boox/compute.py, render.py, suficiencia.py e gap_regulatorio.py.

Uso:
    streamlit run boox/app_streamlit.py

Dois modos de entrada de dados (sidebar):
  1. Demo (Banco Modelo S.A.) - padrao, usa CSVs do repo
  2. Upload de CSVs - arrasta/seleciona seus Books (apenas sessao)
"""
import os
import sys
import csv
import io
import zipfile
import tempfile
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Localizar a raiz do projeto
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from boox.compute import carregar
from boox.render import render_20box, render_csv, render_parecer
from boox.suficiencia import analisar, render_md
from boox.gap_regulatorio import analisar as analisar_gap, render_md as render_gap_md
from boox import _campos as campos_mod

DEMO_PASTA = str(ROOT / "examples" / "banco_modelo_sa")
CANONICO = str(ROOT / "canonico")

CSVS_OBRIGATORIOS_MIN = {
    "B1_processos.csv",
    "B6_riscos.csv",
    "B6_vinculo_processo_risco.csv",
    "B5_controles.csv",
    "B2_apontamentos.csv",
}

# ---------------------------------------------------------------------------
# Config global da pagina
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="BooX — Risco Operacional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      :root {
        --boox-primary: #0f3d3e;
        --boox-accent: #1d9e75;
        --boox-ink: #1f2a30;
        --boox-soft: #f0f7f4;
      }
      .block-container { padding-top: 1.5rem; }
      h1, h2, h3 { color: var(--boox-primary); }
      .boox-hero {
        background: linear-gradient(135deg, #0f3d3e 0%, #1d9e75 100%);
        color: #fff;
        padding: 18px 22px;
        border-radius: 10px;
        margin-bottom: 18px;
      }
      .boox-hero h1 { color: #fff; margin: 0 0 4px; font-size: 24pt; }
      .boox-hero p  { color: #e8f3ee; margin: 0; font-size: 11pt; }
      .boox-badge {
        display:inline-block; background: #fff2; color: #fff;
        padding: 2px 9px; border-radius: 10px; font-size: 9pt;
        margin-left: 8px; vertical-align: middle;
      }
      .metric-tile {
        background: var(--boox-soft);
        border-left: 4px solid var(--boox-accent);
        padding: 10px 14px; border-radius: 0 6px 6px 0;
      }
      .metric-tile .lab { color: #5a6b66; font-size: 10pt; margin: 0; }
      .metric-tile .val { color: var(--boox-primary); font-size: 22pt; font-weight: 600; margin: 0; line-height: 1.1; }
      .source-badge {
        display:inline-block; padding:3px 10px; border-radius:12px;
        font-size:9pt; font-weight:600; margin-left:6px;
      }
      .source-demo    { background:#e4f3ef; color:#0d5a43; }
      .source-upload  { background:#eef2fa; color:#1e3a8a; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
_ver = "?"
try:
    _ver = (ROOT / "canonico" / "VERSION").read_text().strip()
except Exception:
    pass

st.markdown(
    f"""
    <div class="boox-hero">
      <h1>BooX <span class="boox-badge">framework aberto</span></h1>
      <p>Risco operacional e controles internos para instituições financeiras brasileiras ·
      canônico v{_ver} · <a href="https://github.com/walterCNeto/BooX" style="color:#e8f3ee">github.com/walterCNeto/BooX</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Fonte de dados")
    modo = st.radio(
        "Como você quer alimentar o BooX?",
        ["Demo (Banco Modelo S.A.)", "Upload dos meus CSVs"],
        index=0,
        help=(
            "Demo: usa a instância fictícia do repositório. "
            "Upload: carrega seus CSVs pela interface (ficam só na sessão, não vão para o servidor permanentemente)."
        ),
    )

    pasta = None
    status_msg = None

    if modo.startswith("Demo"):
        pasta = DEMO_PASTA
        status_msg = ("source-demo", "Instância de demonstração (dados fictícios)")
    else:  # Upload
        st.caption(
            "Arraste todos os CSVs dos seus Books de uma vez (`B1_processos.csv`, "
            "`B6_riscos.csv`, etc.). Os arquivos ficam na sessão do seu navegador — "
            "**não são persistidos** no servidor."
        )
        arquivos = st.file_uploader(
            "Arraste os CSVs aqui",
            type=["csv"],
            accept_multiple_files=True,
            help="Nomes esperados conforme o padrão do BooX — baixe o ZIP de referência abaixo.",
        )
        if arquivos:
            if "_tmpdir" not in st.session_state:
                st.session_state["_tmpdir"] = tempfile.mkdtemp(prefix="boox_")
            tmp = st.session_state["_tmpdir"]
            nomes_recebidos = set()
            for f in arquivos:
                destino = os.path.join(tmp, f.name)
                with open(destino, "wb") as out:
                    out.write(f.getbuffer())
                nomes_recebidos.add(f.name)
            faltam_min = CSVS_OBRIGATORIOS_MIN - nomes_recebidos
            if faltam_min:
                st.warning(
                    f"Faltam CSVs mínimos para o 20-box: {', '.join(sorted(faltam_min))}. "
                    "O app pode mostrar diagnósticos parciais."
                )
            else:
                st.success(f"{len(arquivos)} CSV(s) carregado(s) nesta sessão.")
            pasta = tmp
            status_msg = ("source-upload", f"Upload — {len(arquivos)} CSV(s) na sessão")
        else:
            st.info("Arraste os CSVs acima para começar. Enquanto isso, a Demo continua carregada.")
            pasta = DEMO_PASTA
            status_msg = ("source-demo", "Demo (upload vazio)")

    st.markdown("---")
    st.markdown("### Templates para preencher")
    st.caption(
        "Para começar com seus próprios dados, baixe o ZIP com os CSVs da Demo "
        "como referência de estrutura. Depois preencha com seus dados reais e "
        "faça upload."
    )

    @st.cache_data(show_spinner=False)
    def _demo_zip():
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(os.listdir(DEMO_PASTA)):
                if f.endswith(".csv"):
                    z.write(os.path.join(DEMO_PASTA, f), arcname=f)
        return buf.getvalue()

    st.download_button(
        "⬇️ Baixar CSVs da Demo (ZIP)",
        data=_demo_zip(),
        file_name="boox_demo_banco_modelo_sa.zip",
        mime="application/zip",
        use_container_width=True,
    )

    st.markdown("---")
    st.caption("MIT (código) · CC BY 4.0 (dados do canônico)")

if status_msg:
    cls, txt = status_msg
    st.markdown(f'<span class="source-badge {cls}">● {txt}</span>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Carregando Books...")
def carregar_instancia(_pasta):
    inst = carregar(_pasta)
    res = inst.computar()
    alertas = inst.alertas_descobertura()
    return res, alertas, {
        "processos": len(inst.processos),
        "riscos": len(inst.riscos),
        "vinculos": len(inst.vinculos),
        "controles": len(inst.controles),
        "apontamentos": len(inst.apontamentos),
        "indicadores": len(inst.indicadores),
        "externos": len(inst.externos),
        "bmap": len(inst.bmap),
    }

@st.cache_data(show_spinner=False)
def carregar_visoes(_pasta):
    arq = os.path.join(_pasta, "B7_visoes.csv")
    if not os.path.exists(arq):
        return []
    with open(arq, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))

@st.cache_data(show_spinner=False)
def carregar_canonico():
    def _ler(nome):
        p = os.path.join(CANONICO, nome)
        if not os.path.exists(p): return []
        with open(p, encoding="utf-8") as f:
            return list(csv.DictReader(f, delimiter=";"))
    return {
        "dominios":    _ler("B_ORG_dominios.csv"),
        "areas":       _ler("B_ORG_areas.csv"),
        "riscos":      _ler("B6_riscos_canonico.csv"),
        "disciplinas": _ler("B9_disciplinas_canonico.csv"),
        "fatores":     _ler("B_FR_canonico.csv"),
        "testes":      _ler("B_TESTES_canonico.csv"),
    }

try:
    res, alertas, counts = carregar_instancia(pasta)
except Exception as e:
    st.error(f"Não consegui carregar os Books em `{pasta}`. Detalhe: {e}")
    st.stop()

visoes = carregar_visoes(pasta)
canon = carregar_canonico()

# ---------------------------------------------------------------------------
# Abas
# ---------------------------------------------------------------------------
tab_mapa, tab_gap, tab_suf, tab_canon = st.tabs(
    ["🗺️ 20-box", "📋 Gap Regulatório", "🔎 Suficiência", "📚 Canônico"]
)

# ===========================================================================
# ABA 1 — 20-BOX
# ===========================================================================
with tab_mapa:
    col_filtros, col_metricas = st.columns([2, 3])
    with col_filtros:
        visao_opts = [("Casa toda", None)] + [(v["nome"], v["id"]) for v in visoes]
        visao_label = st.selectbox(
            "Visão (recorte)",
            [v[0] for v in visao_opts],
            help="Recortes definidos em B7_visoes.csv.",
        )
        visao_id = dict(visao_opts)[visao_label]

    def _aplicar_visao(res_, visao_id_):
        if not visao_id_:
            return res_, "Casa toda"
        arq = os.path.join(pasta, "B7_visao_filtros.csv")
        if not os.path.exists(arq):
            return res_, visao_label
        with open(arq, encoding="utf-8") as f:
            filtros = [r for r in csv.DictReader(f, delimiter=";") if r["visao_id"] == visao_id_]
        if not filtros:
            return res_, visao_label
        def passa(r):
            por_dim = {}
            for f in filtros:
                por_dim.setdefault(f["dimensao"], []).append(f)
            for dim, fs in por_dim.items():
                ok = False
                for f in fs:
                    val = f["valor"]; op = f["operador"]
                    alvo = {"processo": r["processo_id"], "disciplina": r["disciplina"],
                            "risco": r["risco_id"]}.get(dim, "")
                    if op == "igual" and alvo == val: ok = True
                    elif op == "prefixo" and alvo.startswith(val): ok = True
                    elif op == "em" and alvo in val.split("|"): ok = True
                if not ok: return False
            return True
        return [r for r in res_ if passa(r)], visao_label

    res_filtrado, titulo_visao = _aplicar_visao(res, visao_id)

    from collections import Counter
    prio = Counter(r["prioridade"] for r in res_filtrado)
    cob_media = round(sum(r.get("cobertura_pct", 0) for r in res_filtrado) / len(res_filtrado), 1) if res_filtrado else 0

    with col_metricas:
        c1, c2, c3, c4, c5 = st.columns(5)
        for col, label, val in [
            (c1, "Críticos", prio.get("Critico", 0)),
            (c2, "Altos",   prio.get("Alto", 0)),
            (c3, "Médios",  prio.get("Medio", 0)),
            (c4, "Baixos",  prio.get("Baixo", 0)),
            (c5, "OK",      prio.get("OK", 0)),
        ]:
            col.markdown(f'<div class="metric-tile"><p class="lab">{label}</p><p class="val">{val}</p></div>', unsafe_allow_html=True)

    st.markdown("")

    import tempfile as _tf
    with _tf.TemporaryDirectory() as tmp:
        html_path = os.path.join(tmp, "20box.html")
        render_20box(res_filtrado, f"Instância — {titulo_visao}",
                     html_path, alertas_descobertura=alertas if not visao_id else None)
        html_content = open(html_path, encoding="utf-8").read()
    st.components.v1.html(html_content, height=850, scrolling=True)

    criticos = sorted(
        [r for r in res_filtrado if r["prioridade"] in ("Critico", "Alto")],
        key=lambda x: -x["score_x"],
    )
    st.markdown(f"### Pares que exigem tratamento — {len(criticos)}")
    st.caption(f"Cobertura média (validação independente): **{cob_media}%**")
    if criticos:
        import pandas as pd
        df = pd.DataFrame([{
            "Prioridade": r["prioridade"],
            "Processo": r["processo_id"],
            "Risco local": r["risco_id"],
            "Risco canônico": r["risco_canonico"],
            "Impacto": r["nivel_y"],
            "Ambiente": r["nivel_x"],
            "score_x": r["score_x"],
            "Cobertura %": r.get("cobertura_pct", 0),
            "Área": r["area_afetada"],
        } for r in criticos])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum par em prioridade crítica ou alta neste recorte.")

    if alertas and not visao_id:
        st.markdown("### Decisões pendentes")
        st.caption("Sinais (KRI, externos) sem apontamento associado — decisão: abrir apontamento ou justificar.")
        import pandas as pd
        df_al = pd.DataFrame([{
            "Tipo": a["tipo"], "Processo": a["par"][0],
            "Risco": a["par"][1], "Detalhe": a["detalhe"],
        } for a in alertas])
        st.dataframe(df_al, use_container_width=True, hide_index=True)

# ===========================================================================
# ABA 2 — GAP REGULATORIO
# ===========================================================================
with tab_gap:
    col_tipo, col_info = st.columns([1, 3])
    with col_tipo:
        tipos = campos_mod.ENUM.get("tipo_instituicao", ["corretora", "banco_multiplo"])
        default_idx = tipos.index("corretora") if "corretora" in tipos else 0
        tipo = st.selectbox("Tipo de instituição", tipos, index=default_idx)
    with col_info:
        st.info(
            "O gap regulatório cruza os **testes canônicos aplicáveis** ao tipo de instituição "
            "com o que o banco **declara executar** (B_TESTES_execucao). "
            "Testes BSM PQO 2025 Cap 1 estão **ativos e rastreados**; seeds ainda estão como proposto."
        )

    rel = analisar_gap(pasta, tipo_instituicao=tipo)
    if rel.get("erro"):
        st.error(rel["erro"])
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f'<div class="metric-tile"><p class="lab">Testes aplicáveis</p><p class="val">{rel["testes_aplicaveis"]}</p></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-tile"><p class="lab">Requisitos não atendidos</p><p class="val">{len(rel["requisitos_nao_atendidos"])}</p></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-tile"><p class="lab">Controles sem teste</p><p class="val">{len(rel["controles_internos_nao_mapeados"])}</p></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="metric-tile"><p class="lab">FR descobertos</p><p class="val">{len(rel["fatores_risco_descobertos"])}</p></div>', unsafe_allow_html=True)

        st.markdown("### Cobertura por regulador")
        import pandas as pd
        rows = []
        for reg, s in sorted(rel["cobertura_por_regulador"].items()):
            pct = round(100 * s["atendido"] / s["total"], 1) if s["total"] else 0
            rows.append({
                "Regulador": reg, "Total": s["total"],
                "Atendido": f'{s["atendido"]} ({pct}%)',
                "Parcial": s["parcial"], "Não conforme": s["nao_conforme"],
                "Sem execução": s["sem_execucao"], "N/A": s["na"],
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # --- NOVO: requisitos regulatorios nao atendidos (todos, por criticidade) ---
        na = rel["requisitos_nao_atendidos"]
        if na:
            st.markdown(f"### Requisitos regulatórios não atendidos — {len(na)}")
            st.caption("Testes canônicos aplicáveis que **não** estão em estado 'atendido' — inclui parcial, não conforme e sem execução, todas as criticidades.")
            por_c = rel["requisitos_nao_atendidos_por_criticidade"]
            crit_opt = st.radio(
                "Filtrar por criticidade",
                ["Todas", "Alta", "Média", "Baixa"],
                horizontal=True, key="crit_filtro",
            )
            if crit_opt == "Alta": na_filt = por_c.get("alta", [])
            elif crit_opt == "Média": na_filt = por_c.get("media", [])
            elif crit_opt == "Baixa": na_filt = por_c.get("baixa", [])
            else: na_filt = na
            df_na = pd.DataFrame([{
                "Criticidade": r["criticidade"],
                "Regulador": r["regulador"],
                "Teste": r["teste_id"],
                "Norma": r["norma_id"],
                "Título": r["titulo"],
                "Estado": r["estado"],
            } for r in na_filt])
            st.dataframe(df_na, use_container_width=True, hide_index=True)

        # --- RENOMEADO: controles internos (nao regulatorios) com inferencia por moldura ---
        im = rel["controles_internos_nao_mapeados"]
        if im:
            am = rel["controles_internos_atendem_moldura"]
            sm = rel["controles_internos_sem_moldura"]
            st.markdown(f"### Controles internos (não regulatórios) — {len(im)}")
            st.caption(
                "Controles do banco sem teste canônico específico mapeado. "
                "A inferência por moldura regulatória classifica cada um: controles ligados a "
                "risco operacional, cyber, PLD ou LGPD atendem a norma-moldura correspondente, "
                "mesmo sem teste pontual. Controles **sem moldura** são candidatos a revisão."
            )
            col_a, col_b = st.columns(2)
            col_a.markdown(f'<div class="metric-tile"><p class="lab">Atendem norma-moldura</p><p class="val">{len(am)}</p></div>', unsafe_allow_html=True)
            col_b.markdown(f'<div class="metric-tile"><p class="lab">Sem moldura (revisar)</p><p class="val">{len(sm)}</p></div>', unsafe_allow_html=True)

            if rel["molduras_inferidas"]:
                st.markdown("**Agregado por moldura inferida:**")
                df_mold = pd.DataFrame(
                    [{"Moldura": k, "Qtd controles": v}
                     for k, v in sorted(rel["molduras_inferidas"].items(), key=lambda x: -x[1])]
                )
                st.dataframe(df_mold, use_container_width=True, hide_index=True)

            with st.expander(f"Lista detalhada — {len(im)} controles"):
                df_im = pd.DataFrame([{
                    "ID": c["id"],
                    "Ação": c.get("acao", "")[:80],
                    "Classificação": "atende moldura" if c["classificacao"] == "atende_moldura" else "sem moldura",
                    "Moldura inferida": c.get("moldura_norma", "") or "—",
                    "Risco R0 canônico": c.get("risco_r0_canonico", "") or "—",
                } for c in im])
                st.dataframe(df_im, use_container_width=True, hide_index=True)

        if rel["fatores_risco_descobertos"]:
            with st.expander(f"Fatores de Risco descobertos — {len(rel['fatores_risco_descobertos'])}"):
                st.caption("FRs canônicos cujos testes NÃO estão atendidos — sinal de vulnerabilidade estrutural.")
                df_fr = pd.DataFrame([{
                    "FR": f, "Testes": s["total_testes"], "Atendidos": s["testes_atendidos"],
                } for f, s in rel["fatores_risco_descobertos"]])
                st.dataframe(df_fr, use_container_width=True, hide_index=True)

# ===========================================================================
# ABA 3 — SUFICIENCIA
# ===========================================================================
with tab_suf:
    rel_suf = analisar(pasta)
    r = rel_suf["resumo"]
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-tile"><p class="lab">Books presentes</p><p class="val">{r["books_presentes"]}/{r["books_total"]}</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-tile"><p class="lab">Obrig. completos</p><p class="val">{r["obrigatorios_completos"]}/{r["obrigatorios_total"]}</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-tile"><p class="lab">Alertas estruturais</p><p class="val">{len(rel_suf["alertas"])}</p></div>', unsafe_allow_html=True)

    st.markdown("### Diagnóstico por Book")
    st.caption("Lê os Books preenchidos e diagnostica qualidade dos dados **antes** de confiar no 20-box.")
    import pandas as pd
    emoji = {"completo": "🟢 OK", "valido_baixa_confianca": "🟡 ATENÇÃO",
             "incompleto": "🔴 FALHA", "ausente": "⚪ AUSENTE"}

    def _fmt_pct(v):
        """Sempre string: evita ArrowInvalid por coluna mista int/str."""
        if v is None or v == "-":
            return "—"
        try:
            return f"{int(v)}%"
        except (ValueError, TypeError):
            return str(v)

    rows = []
    for b in rel_suf["books"]:
        if not b["presente"]:
            rows.append({"Book": b["titulo"], "Status": emoji["ausente"], "Registros": 0,
                         "Obrig. mín.": "—", "Recom. médio": "—"})
        else:
            rows.append({
                "Book": b["titulo"], "Status": emoji.get(b["status"], b["status"]),
                "Registros": b["registros"],
                "Obrig. mín.": _fmt_pct(b.get("preenchimento_obrigatorio_min")),
                "Recom. médio": _fmt_pct(b.get("preenchimento_recomendado_medio")),
            })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    if rel_suf["alertas"]:
        st.markdown("### Alertas estruturais")
        for tipo_al, msg in rel_suf["alertas"]:
            st.warning(f"**[{tipo_al}]** {msg}")

    st.markdown("### Contagens da instância")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Processos", counts["processos"])
    c2.metric("Riscos", counts["riscos"])
    c3.metric("Pares (vínculos)", counts["vinculos"])
    c4.metric("Controles", counts["controles"])
    c1.metric("Apontamentos", counts["apontamentos"])
    c2.metric("Indicadores", counts["indicadores"])
    c3.metric("Externos", counts["externos"])
    c4.metric("B_MAP", counts["bmap"])

# ===========================================================================
# ABA 4 — CANONICO
# ===========================================================================
with tab_canon:
    st.markdown(
        "Camada **canônica** do BooX: o vocabulário comum que serve a todo banco. "
        "Cada ID aqui pode ser referenciado via B_MAP pelo vocabulário local do banco."
    )

    sub = st.selectbox(
        "Explorar",
        ["Riscos (hierarquia R0 → R4)", "Áreas organizacionais", "Disciplinas",
         "Fatores de Risco", "Testes regulamentares"],
    )

    import pandas as pd
    if sub.startswith("Riscos"):
        st.caption(f"{len(canon['riscos'])} riscos canônicos (R0 a R4). Hoje foca em Cyber, Conformidade e PLD-FT na granularidade fina.")
        df = pd.DataFrame(canon["riscos"])[["id", "nome", "nivel", "parent_id", "categoria_basileia", "status"]]
        nivel_filtro = st.multiselect("Filtrar por nível", sorted(df["nivel"].unique()), default=sorted(df["nivel"].unique()))
        df = df[df["nivel"].isin(nivel_filtro)]
        st.dataframe(df, use_container_width=True, hide_index=True, height=500)

    elif sub.startswith("Áreas"):
        st.caption(f"{len(canon['areas'])} áreas canônicas distribuídas em {len(canon['dominios'])} domínios (1ª, 2ª e 3ª linhas de defesa).")
        df = pd.DataFrame(canon["areas"])[["id", "nome", "dominio_id", "descricao"]]
        st.dataframe(df, use_container_width=True, hide_index=True, height=500)

    elif sub.startswith("Disciplinas"):
        st.caption(f"{len(canon['disciplinas'])} disciplinas transversais (crédito, mercado, cyber, PLD, LGPD, ...)")
        df = pd.DataFrame(canon["disciplinas"])
        st.dataframe(df, use_container_width=True, hide_index=True, height=500)

    elif sub.startswith("Fatores"):
        st.caption(f"{len(canon['fatores'])} Fatores de Risco canônicos (causas-raiz específicas).")
        df = pd.DataFrame(canon["fatores"])
        st.dataframe(df, use_container_width=True, hide_index=True, height=500)

    elif sub.startswith("Testes"):
        ts = canon["testes"]
        ativos = [t for t in ts if t.get("status") == "ativo"]
        propostos = [t for t in ts if t.get("status") == "proposto"]
        st.caption(
            f"**{len(ts)} testes canônicos** — {len(ativos)} ativos rastreados (BSM PQO 2025 Cap 1) e {len(propostos)} seeds propostos."
        )
        status_filtro = st.radio("Status", ["Todos", "Ativo (rastreado)", "Proposto (seed)"], horizontal=True)
        df_src = ts
        if status_filtro == "Ativo (rastreado)":
            df_src = ativos
        elif status_filtro == "Proposto (seed)":
            df_src = propostos
        df = pd.DataFrame(df_src)[
            ["id", "regulador", "norma_id", "artigo", "titulo", "criticidade",
             "aplicabilidade", "status"]
        ]
        st.dataframe(df, use_container_width=True, hide_index=True, height=520)

        with st.expander("Ver detalhes de um teste"):
            tid = st.selectbox("ID do teste", [t["id"] for t in df_src])
            if tid:
                t = next(x for x in df_src if x["id"] == tid)
                st.markdown(f"**{t['titulo']}**")
                st.markdown(f"- **Regulador:** {t['regulador']}  ·  **Norma:** `{t['norma_id']}`  ·  **Artigo:** {t.get('artigo','—')}")
                st.markdown(f"- **Aplicabilidade:** {t['aplicabilidade']}")
                st.markdown(f"- **Criticidade:** {t.get('criticidade','—')}  ·  **Status:** `{t['status']}`")
                st.markdown(f"**Descrição:** {t.get('descricao','—')}")
                if t.get("metodo_verificacao"):
                    st.markdown(f"**Método de verificação:** {t['metodo_verificacao']}")
                if t.get("evidencia_esperada"):
                    st.markdown(f"**Evidência esperada:** {t['evidencia_esperada']}")
                if t.get("fonte_url"):
                    st.markdown(f"**Fonte oficial:** {t['fonte_url']}")

# ---------------------------------------------------------------------------
# Rodape
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "BooX · Framework open-source · [MIT](https://github.com/walterCNeto/BooX/blob/main/LICENSE) · "
    "Banco Modelo S.A. e todos seus dados são fictícios e sintéticos."
)
