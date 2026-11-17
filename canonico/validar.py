# -*- coding: utf-8 -*-
"""
validar.py — Verifica a integridade do canonico BooX.

Checa:
  - IDs duplicados (em qualquer arquivo)
  - substituido_por apontando para ID inexistente
  - ID deprecado sem substituto (apenas aviso)
  - hierarquia: area.dominio_id existe; disciplina.dominio_2linha existe
  - parent_id de riscos aponta para risco existente
  - testes: equivale_a existente e sem ciclos; vigencia_* em AAAA-MM-DD

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


    # ---- extensoes fase 1: FR e testes canonicos ----
    import os as _os
    fr_path = _os.path.join(AQUI,"B_FR_canonico.csv")
    ts_path = _os.path.join(AQUI,"B_TESTES_canonico.csv")
    fr = ler("B_FR_canonico.csv") if _os.path.exists(fr_path) else []
    ts = ler("B_TESTES_canonico.csv") if _os.path.exists(ts_path) else []
    if fr:
        checa_dup(fr, "fatores"); checa_subst(fr, "fatores")
        for x in fr:
            rc = x.get("risco_canonico_id","").strip()
            if rc and rc not in ris_ids:
                erros.append(f"[fatores] {x['id']}: risco_canonico_id '{rc}' nao existe")
    fr_ids = {x["id"] for x in fr}
    if ts:
        checa_dup(ts, "testes"); checa_subst(ts, "testes")
        for x in ts:
            rc = x.get("risco_r0_canonico","").strip()
            fc = x.get("fator_risco_canonico_id","").strip()
            if rc and rc not in ris_ids:
                erros.append(f"[testes] {x['id']}: risco_r0_canonico '{rc}' nao existe")
            if fc and fc not in fr_ids:
                erros.append(f"[testes] {x['id']}: fator_risco_canonico_id '{fc}' nao existe")
        ts_ids = {x["id"] for x in ts}
        import datetime as _dt
        def _data_ok(v):
            try: _dt.date.fromisoformat(v); return True
            except ValueError: return False
        for x in ts:
            eq = x.get("equivale_a","").strip()
            if eq:
                if eq not in ts_ids:
                    erros.append(f"[testes] {x['id']}: equivale_a '{eq}' nao existe")
                elif eq == x["id"]:
                    erros.append(f"[testes] {x['id']}: equivale_a aponta para si mesmo")
            for c in ("vigencia_inicio","vigencia_fim"):
                v = x.get(c,"").strip()
                if v and not _data_ok(v):
                    erros.append(f"[testes] {x['id']}: {c} '{v}' nao e data AAAA-MM-DD")
            vi, vf = x.get("vigencia_inicio","").strip(), x.get("vigencia_fim","").strip()
            if vi and vf and _data_ok(vi) and _data_ok(vf) and vf < vi:
                erros.append(f"[testes] {x['id']}: vigencia_fim anterior a vigencia_inicio")
        # ciclos em equivale_a
        eq_map = {x["id"]: x.get("equivale_a","").strip() for x in ts}
        ciclicos = set()
        for i in eq_map:
            vistos, atual = set(), i
            while atual and atual in eq_map and atual not in vistos:
                vistos.add(atual); atual = eq_map[atual]
            if atual and atual in vistos and atual != eq_map.get(atual):
                ciclicos.add(i)
        if ciclicos:
            erros.append(f"[testes] equivale_a ciclico envolvendo: {', '.join(sorted(ciclicos))}")
    if fr or ts:
        propostos_ts = sum(1 for x in ts if x.get("status")=="proposto")
        print(f"  fatores={len(fr)} testes_canonicos={len(ts)} (propostos={propostos_ts})")

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
