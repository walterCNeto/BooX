# -*- coding: utf-8 -*-
"""
validar.py — Verifica a integridade do canonico BooX.

Checa:
  - IDs duplicados (em qualquer arquivo)
  - substituido_por apontando para ID inexistente
  - ID deprecado sem substituto (apenas aviso)
  - hierarquia: area.dominio_id existe; disciplina.dominio_2linha existe
  - parent_id de riscos aponta para risco existente

Uso: python validar.py
Saida: lista de problemas; codigo 0 se tudo ok, 1 se ha erros.
"""
import csv, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))

def ler(arq):
    with open(os.path.join(AQUI, arq), encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))

def main():
    erros, avisos = [], []
    dom = ler("B_ORG_dominios.csv")
    are = ler("B_ORG_areas.csv")
    ris = ler("B6_riscos_canonico.csv")
    dis = ler("B9_disciplinas_canonico.csv")

    def checa_dup(lst, nome):
        ids = [r["id"] for r in lst]
        vistos, dups = set(), set()
        for i in ids:
            if i in vistos: dups.add(i)
            vistos.add(i)
        if dups: erros.append(f"[{nome}] IDs duplicados: {', '.join(sorted(dups))}")

    def checa_subst(lst, nome):
        ids = {r["id"] for r in lst}
        for r in lst:
            sp = r.get("substituido_por","").strip()
            if sp and sp not in ids:
                erros.append(f"[{nome}] {r['id']}: substituido_por '{sp}' nao existe")
            if r.get("status")=="deprecado" and not sp:
                avisos.append(f"[{nome}] {r['id']}: deprecado sem substituto (descontinuado)")

    for lst, nome in [(dom,"dominios"),(are,"areas"),(ris,"riscos"),(dis,"disciplinas")]:
        checa_dup(lst, nome); checa_subst(lst, nome)

    dom_ids = {d["id"] for d in dom}
    are_ids = {a["id"] for a in are}
    ris_ids = {r["id"] for r in ris}

    for a in are:
        if a.get("dominio_id") not in dom_ids:
            erros.append(f"[areas] {a['id']}: dominio_id '{a.get('dominio_id')}' nao existe")
    for d in dis:
        d2 = d.get("dominio_2linha","").strip()
        if d2 and d2 not in are_ids:
            erros.append(f"[disciplinas] {d['id']}: dominio_2linha '{d2}' nao existe")
    for r in ris:
        p = r.get("parent_id","").strip()
        if p and p not in ris_ids:
            erros.append(f"[riscos] {r['id']}: parent_id '{p}' nao existe")

    ver = open(os.path.join(AQUI,"VERSION")).read().strip() if os.path.exists(os.path.join(AQUI,"VERSION")) else "?"
    print(f"Validacao do canonico v{ver}")
    print(f"  dominios={len(dom)} areas={len(are)} riscos={len(ris)} disciplinas={len(dis)}")
    ativos = sum(1 for l in dom+are+ris+dis if l.get("status")=="ativo")
    deprec = sum(1 for l in dom+are+ris+dis if l.get("status")=="deprecado")
    print(f"  ativos={ativos} deprecados={deprec}")
    print()
    if avisos:
        print("AVISOS:")
        for a in avisos: print("  -", a)
        print()
    if erros:
        print("ERROS:")
        for e in erros: print("  -", e)
        print(f"\n{len(erros)} erro(s). Corrija antes de publicar.")
        sys.exit(1)
    print("OK: canonico integro, sem erros.")
    sys.exit(0)

if __name__ == "__main__":
    main()
