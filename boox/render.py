# -*- coding: utf-8 -*-
"""BooX render — gera 20-box HTML (gradiente diagonal), detalhamento CSV e parecer MD."""
import csv, os, colorsys
from collections import Counter, defaultdict

NIVEIS_Y = ["Elevado","Alto","Medio","Baixo","Imaterial"]  # topo->base
NIVEIS_X = ["--","-","0","+","++"]
ROT_X = {"--":"Critico","-":"Atencao","0":"Neutro","+":"Bom","++":"Adequado"}
# cor das bolhas por prioridade (tom forte, para destacar sobre a celula clara)
COR_PRIO = {"Critico":"#A32D2D","Alto":"#C0512A","Medio":"#A06A12","Baixo":"#4E7A1A","OK":"#127A5E"}

def _prioridade(ny,nx):
    Y=["Imaterial","Baixo","Medio","Alto","Elevado"].index(ny)
    X=NIVEIS_X.index(nx)
    M=[
     ["Medio","Medio","Baixo","Baixo","OK"],
     ["Medio","Medio","Baixo","Baixo","OK"],
     ["Alto","Medio","Medio","Baixo","Baixo"],
     ["Critico","Alto","Medio","Medio","Baixo"],
     ["Critico","Critico","Alto","Medio","Medio"],
    ]
    return M[Y][X]

def _lerp(a,b,t): return a+(b-a)*t

def _hsl(h,s,l):
    r,g,b=colorsys.hls_to_rgb(h/360.0,l,s)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def _cor_celula(iy,ix):
    """Gradiente diagonal: vermelho (impacto alto + ambiente ruim) -> verde (oposto).
    Intensidade do fill acompanha o impacto (baixo impacto = lavado)."""
    impacto=(4-iy)/4.0      # 1 = Elevado (topo)
    ambiente=ix/4.0         # 1 = Adequado (direita)
    sev=impacto*0.55+(1-ambiente)*0.45
    hue=_lerp(130,5,sev)            # 130 verde -> 5 vermelho
    alpha=_lerp(0.10,0.42,impacto*0.6+sev*0.4)
    fill=_hsl(hue,0.55,0.5)
    stroke=_hsl(hue,0.45,0.40)
    return fill,stroke,alpha

def render_20box(res, titulo, caminho_html):
    celulas=defaultdict(list)
    for r in res:
        celulas[(r["nivel_y"],r["nivel_x"])].append(r)
    cell_w,cell_h=116,92; x0,y0=150,72
    W=x0+5*cell_w+40; H=y0+5*cell_h+96
    P=[]
    P.append(f'<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI,Arial,sans-serif">')
    P.append(f'<text x="{W/2}" y="32" text-anchor="middle" font-size="18" font-weight="600">{titulo}</text>')
    P.append(f'<text x="{W/2}" y="52" text-anchor="middle" font-size="12" fill="#777">Impacto x Ambiente de Controles — {len(res)} pares processo x risco</text>')
    P.append(f'<text x="24" y="{y0+5*cell_h/2}" text-anchor="middle" font-size="12" fill="#444" transform="rotate(-90 24 {y0+5*cell_h/2})">Impacto</text>')
    for iy,ny in enumerate(NIVEIS_Y):
        cy=y0+iy*cell_h
        P.append(f'<text x="{x0-10}" y="{cy+cell_h/2}" text-anchor="end" font-size="11" fill="#444" dominant-baseline="central">{ny}</text>')
        for ix,nx in enumerate(NIVEIS_X):
            cx=x0+ix*cell_w
            fill,stroke,alpha=_cor_celula(iy,ix)
            P.append(f'<rect x="{cx}" y="{cy}" width="{cell_w-6}" height="{cell_h-6}" rx="8" fill="{fill}" fill-opacity="{alpha:.2f}" stroke="{stroke}" stroke-width="0.7"/>')
            pares=celulas.get((ny,nx),[])
            if pares:
                per_row=3; bx=cx+20; by=cy+24
                for i,p in enumerate(pares[:9]):
                    ox=bx+(i%per_row)*30; oy=by+(i//per_row)*24
                    rad=min(6+p["materialidade"],11)
                    cb=COR_PRIO[p["prioridade"]]
                    tip=f'{p["processo_id"]} x {p["risco_id"]} ({p["risco_canonico"]}) — {p["prioridade"]} — Y={p["nivel_y"]} X={p["nivel_x"]} sx={p["score_x"]}'
                    P.append(f'<circle cx="{ox}" cy="{oy}" r="{rad}" fill="{cb}" fill-opacity="0.78" stroke="#fff" stroke-width="1"><title>{tip}</title></circle>')
                if len(pares)>9:
                    P.append(f'<text x="{cx+cell_w-18}" y="{cy+cell_h-14}" font-size="9" fill="#555">+{len(pares)-9}</text>')
    for ix,nx in enumerate(NIVEIS_X):
        cx=x0+ix*cell_w+cell_w/2
        P.append(f'<text x="{cx}" y="{y0+5*cell_h+18}" text-anchor="middle" font-size="11" fill="#444">{nx} {ROT_X[nx]}</text>')
    P.append(f'<text x="{x0+5*cell_w/2}" y="{y0+5*cell_h+42}" text-anchor="middle" font-size="12" fill="#444">Ambiente de Controles</text>')
    # legenda das bolhas (prioridade)
    ly=y0+5*cell_h+64; lx=x0
    for prio in ["Critico","Alto","Medio","Baixo","OK"]:
        P.append(f'<circle cx="{lx+5}" cy="{ly+5}" r="6" fill="{COR_PRIO[prio]}" fill-opacity="0.78"/>')
        P.append(f'<text x="{lx+16}" y="{ly+9}" font-size="10" fill="#555">{prio}</text>')
        lx+=92
    P.append('</svg>')
    svg="\n".join(P)
    html=f"""<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8">
<title>BooX — {titulo}</title>
<style>body{{margin:0;padding:24px;background:#faf9f6;font-family:Segoe UI,Arial,sans-serif;color:#222}}
.wrap{{max-width:780px;margin:0 auto;background:#fff;border:1px solid #e5e3da;border-radius:14px;padding:24px;box-shadow:0 4px 16px rgba(0,0,0,.04)}}
.bolha{{font-size:12px;color:#777;margin-top:8px}}</style></head>
<body><div class="wrap">{svg}
<p class="bolha">A cor da célula gradua do vermelho (alto impacto e ambiente crítico) ao verde (baixo impacto e ambiente adequado); células de menor impacto são mais claras. Cada bolha é um par processo×risco; o tamanho reflete a materialidade e a cor a prioridade de tratamento. Passe o mouse para detalhes.</p>
</div></body></html>"""
    with open(caminho_html,"w",encoding="utf-8") as f: f.write(html)

def render_csv(res, caminho):
    with open(caminho,"w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,delimiter=";")
        w.writerow(["processo_id","processo_nome","risco_id","risco_canonico","disciplina",
                    "area_afetada","area_gestora","materialidade","score_y","nivel_y",
                    "score_x","nivel_x","prioridade"])
        for r in sorted(res,key=lambda x:-x["score_x"]):
            w.writerow([r["processo_id"],r["processo_nome"],r["risco_id"],r["risco_canonico"],
                        r["disciplina"],r["area_afetada"],r["area_gestora"],r["materialidade"],
                        r["score_y"],r["nivel_y"],r["score_x"],r["nivel_x"],r["prioridade"]])

def render_parecer(res, titulo, caminho):
    prio=Counter(r["prioridade"] for r in res)
    criticos=[r for r in res if r["prioridade"] in ("Critico","Alto")]
    criticos.sort(key=lambda x:-x["score_x"])
    L=[f"# Parecer BooX — {titulo}",""]
    L.append(f"Pares processo x risco avaliados: **{len(res)}**.")
    L.append("")
    L.append("## Distribuicao de Prioridade de Tratamento")
    L.append("")
    for p in ["Critico","Alto","Medio","Baixo","OK"]:
        if prio.get(p): L.append(f"- **{p}**: {prio[p]}")
    L.append("")
    if criticos:
        L.append("## Pares que exigem tratamento (Critico e Alto)")
        L.append("")
        for r in criticos:
            L.append(f"### {r['risco_canonico']} em {r['processo_id']} — {r['prioridade']}")
            L.append(f"- Risco local: {r['risco_nome']} ({r['risco_id']})")
            L.append(f"- Processo: {r['processo_nome']}")
            L.append(f"- Impacto: {r['nivel_y']} · Ambiente: {r['nivel_x']} ({ROT_X[r['nivel_x']]}) · score_x={r['score_x']}")
            L.append(f"- Area afetada: {r['area_afetada']} · Area gestora: {r['area_gestora']}")
            L.append("")
    L.append("---")
    L.append("_Gerado pelo BooX a partir do Banco Modelo S.A. (dados sinteticos)._")
    with open(caminho,"w",encoding="utf-8") as f: f.write("\n".join(L))
