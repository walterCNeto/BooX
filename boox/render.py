# -*- coding: utf-8 -*-
"""BooX render v0.2 — 20-box com gradiente diagonal + bolhas-pizza de cobertura.

Cada bolha e uma pizza: preenchimento preto = % de cobertura (validacao
independente); cinza = nao coberto. Contorno colorido = prioridade.
"""
import csv, os, math, colorsys
from collections import Counter, defaultdict

NIVEIS_Y = ["Elevado","Alto","Medio","Baixo","Imaterial"]
NIVEIS_X = ["--","-","0","+","++"]
ROT_X = {"--":"Critico","-":"Atencao","0":"Neutro","+":"Bom","++":"Adequado"}
COR_PRIO = {"Critico":"#A32D2D","Alto":"#C0512A","Medio":"#A06A12","Baixo":"#4E7A1A","OK":"#127A5E"}

def _lerp(a,b,t): return a+(b-a)*t
def _hsl(h,s,l):
    r,g,b=colorsys.hls_to_rgb(h/360.0,l,s)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def _cor_celula(iy,ix):
    impacto=(4-iy)/4.0; ambiente=ix/4.0
    sev=impacto*0.55+(1-ambiente)*0.45
    hue=_lerp(130,5,sev)
    alpha=_lerp(0.10,0.42,impacto*0.6+sev*0.4)
    return _hsl(hue,0.55,0.5), _hsl(hue,0.45,0.40), alpha

def _pizza_svg(ox,oy,rad,pct,contorno,tip=""):
    parts=[]
    title=f"<title>{tip}</title>" if tip else ""
    parts.append(f'<circle cx="{ox}" cy="{oy}" r="{rad}" fill="#d8d8d8" stroke="{contorno}" stroke-width="1.3">{title}</circle>')
    if pct>=100:
        parts.append(f'<circle cx="{ox}" cy="{oy}" r="{rad}" fill="#1a1a1a" stroke="{contorno}" stroke-width="1.3">{title}</circle>')
    elif pct>0:
        ang=2*math.pi*pct/100.0
        x1=ox; y1=oy-rad
        x2=ox+rad*math.sin(ang); y2=oy-rad*math.cos(ang)
        large=1 if ang>math.pi else 0
        path=f"M {ox},{oy} L {x1},{y1} A {rad},{rad} 0 {large} 1 {x2:.2f},{y2:.2f} Z"
        parts.append(f'<path d="{path}" fill="#1a1a1a">{title}</path>')
    return "".join(parts)

def render_20box(res, titulo, caminho_html, alertas_descobertura=None):
    celulas=defaultdict(list)
    for r in res:
        celulas[(r["nivel_y"], r["nivel_x"])].append(r)
    cell_w, cell_h = 122, 96
    x0, y0 = 150, 72
    W = x0 + 5*cell_w + 110
    H = y0 + 5*cell_h + 145
    P=[f'<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI,Arial,sans-serif">']
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
            if not pares: continue
            MAX=6; per=3; bx=cx+22; by=cy+30
            for i,p in enumerate(pares[:MAX]):
                ox=bx+(i%per)*32; oy=by+(i//per)*28
                rad=min(7+p["materialidade"],12)
                pct=p.get("cobertura_pct",0)
                tip=(f'{p["processo_id"]} x {p["risco_id"]} ({p["risco_canonico"]}) — '
                     f'{p["prioridade"]} — Y={p["nivel_y"]} X={p["nivel_x"]} '
                     f'sx={p["score_x"]} — cobertura {pct}%')
                P.append(_pizza_svg(ox,oy,rad,pct,COR_PRIO[p["prioridade"]],tip))
            if len(pares)>MAX:
                P.append(f'<text x="{cx+cell_w-22}" y="{cy+cell_h-12}" font-size="10" fill="#333" font-weight="600">+{len(pares)-MAX}</text>')
    for ix,nx in enumerate(NIVEIS_X):
        cx=x0+ix*cell_w+cell_w/2
        P.append(f'<text x="{cx}" y="{y0+5*cell_h+20}" text-anchor="middle" font-size="11" fill="#444">{nx} {ROT_X[nx]}</text>')
    P.append(f'<text x="{x0+5*cell_w/2}" y="{y0+5*cell_h+44}" text-anchor="middle" font-size="12" fill="#444">Ambiente de Controles</text>')
    # Legenda linha 1 — prioridade (circulo 100% colorido, SEM pizza)
    ly=y0+5*cell_h+70; lx=x0
    P.append(f'<text x="{lx}" y="{ly+9}" font-size="10" fill="#555" font-weight="600">Prioridade:</text>')
    lx+=78
    for prio in ["Critico","Alto","Medio","Baixo","OK"]:
        c=COR_PRIO[prio]
        P.append(f'<circle cx="{lx+7}" cy="{ly+5}" r="7" fill="{c}" stroke="{c}" stroke-width="1.3"/>')
        P.append(f'<text x="{lx+20}" y="{ly+9}" font-size="10" fill="#555">{prio}</text>')
        lx+=70

    # Legenda linha 2 — cobertura (pizza progressiva, cinza+preto, sem cor)
    ly=y0+5*cell_h+96; lx=x0
    P.append(f'<text x="{lx}" y="{ly+9}" font-size="10" fill="#555" font-weight="600">Cobertura:</text>')
    lx+=78
    for pct in [0,25,50,75,100]:
        P.append(_pizza_svg(lx+7,ly+5,7,pct,"#888"))
        P.append(f'<text x="{lx+20}" y="{ly+9}" font-size="10" fill="#555">{pct}%</text>')
        lx+=56

    # Nota conceitual explicando que as duas dimensoes se combinam na bolha
    ly=y0+5*cell_h+120; lx=x0
    P.append(f'<text x="{lx}" y="{ly}" font-size="9" fill="#777" font-style="italic">Cada bolha do mapa combina as duas dimensoes: contorno colorido = prioridade · preenchimento preto = cobertura.</text>')

    P.append('</svg>')
    svg="\n".join(P)
    bloco=""
    if alertas_descobertura:
        tot=len(alertas_descobertura)
        kri=sum(1 for a in alertas_descobertura if a["tipo"]=="kri")
        ext=sum(1 for a in alertas_descobertura if a["tipo"]=="externo")
        bloco=f"""<div class="alertas">
<div class="al-title">Decisoes pendentes ({tot}): sinais sem apontamento associado</div>
<div class="al-sub">Cada um e uma escolha: abrir apontamento (para tratar) ou justificar (apetite a revisar). KRIs no vermelho/amarelo: {kri}. Sinais externos relevantes: {ext}.</div>
<ul>"""
        for a in alertas_descobertura[:15]:
            p,r=a["par"]
            bloco+=f'<li><b>[{a["tipo"]}]</b> {p} x {r} — {a["detalhe"]}</li>'
        if tot>15: bloco+=f"<li>... e mais {tot-15} alerta(s).</li>"
        bloco+="</ul></div>"
    html=f"""<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8">
<title>BooX — {titulo}</title>
<style>
body{{margin:0;padding:24px;background:#faf9f6;font-family:Segoe UI,Arial,sans-serif;color:#222}}
.wrap{{max-width:920px;margin:0 auto;background:#fff;border:1px solid #e5e3da;border-radius:14px;padding:24px;box-shadow:0 4px 16px rgba(0,0,0,.04)}}
.bolha{{font-size:12px;color:#777;margin-top:12px;line-height:1.5}}
.alertas{{margin-top:18px;padding:14px 16px;background:#fdf6ec;border-left:4px solid #c08018;border-radius:0 6px 6px 0;font-size:12px}}
.al-title{{font-weight:600;color:#7a4f10;margin-bottom:2px;font-size:13px}}
.al-sub{{color:#7a4f10;font-size:11px;margin-bottom:6px}}
.alertas ul{{margin:6px 0 0 0;padding-left:22px;color:#444}}
.alertas li{{margin:2px 0}}
</style></head>
<body><div class="wrap">{svg}
<p class="bolha">A cor da celula gradua do vermelho (alto impacto e ambiente critico) ao verde (baixo impacto e ambiente adequado). Cada bolha e um par processo x risco; o tamanho reflete a materialidade, o contorno reflete a prioridade de tratamento, e o preto na pizza reflete o grau de cobertura (validacao independente). Passe o mouse para detalhes.</p>
{bloco}
</div></body></html>"""
    with open(caminho_html,"w",encoding="utf-8") as f: f.write(html)

def render_csv(res, caminho):
    with open(caminho,"w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,delimiter=";")
        w.writerow(["processo_id","processo_nome","risco_id","risco_canonico","disciplina",
                    "area_afetada","area_gestora","materialidade","cobertura_pct",
                    "score_y","nivel_y","score_x","nivel_x","prioridade"])
        for r in sorted(res,key=lambda x:-x["score_x"]):
            w.writerow([r["processo_id"],r["processo_nome"],r["risco_id"],r["risco_canonico"],
                        r["disciplina"],r["area_afetada"],r["area_gestora"],r["materialidade"],
                        r.get("cobertura_pct",0),
                        r["score_y"],r["nivel_y"],r["score_x"],r["nivel_x"],r["prioridade"]])

def render_parecer(res, titulo, caminho, alertas_descobertura=None):
    prio=Counter(r["prioridade"] for r in res)
    cob_media=round(sum(r.get("cobertura_pct",0) for r in res)/len(res),1) if res else 0
    criticos=sorted([r for r in res if r["prioridade"] in ("Critico","Alto")], key=lambda x:-x["score_x"])
    L=[f"# Parecer BooX — {titulo}",""]
    L.append(f"Pares processo x risco avaliados: **{len(res)}**.")
    L.append(f"Cobertura media (validacao independente): **{cob_media}%**.")
    L.append("")
    L.append("## Distribuicao de Prioridade de Tratamento"); L.append("")
    for p in ["Critico","Alto","Medio","Baixo","OK"]:
        if prio.get(p): L.append(f"- **{p}**: {prio[p]}")
    L.append("")
    if criticos:
        L.append("## Pares que exigem tratamento (Critico e Alto)"); L.append("")
        for r in criticos:
            L.append(f"### {r['risco_canonico']} em {r['processo_id']} — {r['prioridade']}")
            L.append(f"- Risco local: {r['risco_nome']} ({r['risco_id']})")
            L.append(f"- Processo: {r['processo_nome']}")
            L.append(f"- Impacto: {r['nivel_y']} · Ambiente: {r['nivel_x']} ({ROT_X[r['nivel_x']]}) · score_x={r['score_x']}")
            L.append(f"- Cobertura: {r.get('cobertura_pct',0)}%")
            L.append(f"- Area afetada: {r['area_afetada']} · Area gestora: {r['area_gestora']}")
            L.append("")
    if alertas_descobertura:
        L.append("## Decisoes pendentes"); L.append("")
        L.append(f"Existem **{len(alertas_descobertura)} sinais** (KRIs no vermelho/amarelo, externos relevantes) **sem apontamento associado**. Cada um e uma decisao: abrir apontamento para tratar, ou justificar (apetite a revisar).")
        L.append("")
        for a in alertas_descobertura[:20]:
            p,r=a["par"]
            L.append(f"- [{a['tipo']}] {p} × {r} — {a['detalhe']}")
        L.append("")
    L.append("---"); L.append("_Gerado pelo BooX._")
    with open(caminho,"w",encoding="utf-8") as f: f.write("\n".join(L))
