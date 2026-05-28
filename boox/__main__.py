# -*- coding: utf-8 -*-
import sys, os
from boox.compute import carregar
from boox.render import render_20box, render_csv, render_parecer

def main():
    if len(sys.argv)<2:
        print("uso: python -m boox <pasta_da_instancia> [--out <pasta_saida>] [--visao <ID>]")
        sys.exit(1)
    pasta=sys.argv[1]
    out="output"
    visao=None
    if "--out" in sys.argv: out=sys.argv[sys.argv.index("--out")+1]
    if "--visao" in sys.argv: visao=sys.argv[sys.argv.index("--visao")+1]
    os.makedirs(out,exist_ok=True)
    inst=carregar(pasta)
    res=inst.computar()
    titulo="Banco Modelo S.A. — Casa toda"
    if visao:
        res,titulo=aplicar_visao(inst,res,visao)
    render_20box(res,titulo,os.path.join(out,"20box.html"))
    render_csv(res,os.path.join(out,"detalhamento.csv"))
    render_parecer(res,titulo,os.path.join(out,"parecer.md"))
    print(f"Gerado em {out}/ : 20box.html, detalhamento.csv, parecer.md")
    print(f"Pares: {len(res)}")

def aplicar_visao(inst,res,visao_id):
    filtros=[f for f in inst.filtros if f["visao_id"]==visao_id]
    vis=next((v for v in inst.visoes if v["id"]==visao_id),None)
    titulo=f"Banco Modelo S.A. — {vis['nome'] if vis else visao_id}"
    if not filtros: return res,titulo
    def passa(r):
        # AND entre dimensoes, OR dentro da mesma dimensao
        por_dim={}
        for f in filtros:
            por_dim.setdefault(f["dimensao"],[]).append(f)
        for dim,fs in por_dim.items():
            ok=False
            for f in fs:
                val=f["valor"]; op=f["operador"]
                alvo={"processo":r["processo_id"],"disciplina":r["disciplina"],
                      "risco":r["risco_id"]}.get(dim,"")
                if op=="igual" and alvo==val: ok=True
                elif op=="prefixo" and alvo.startswith(val): ok=True
                elif op=="em" and alvo in val.split("|"): ok=True
            if not ok: return False
        return True
    return [r for r in res if passa(r)], titulo

if __name__=="__main__": main()
