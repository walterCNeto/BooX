# -*- coding: utf-8 -*-
"""
curar.py — Curadoria controlada do canonico BooX (Rota A).

Aplica mudancas seguindo as regras de canonico/REGRAS.md:
  - adicionar  : inclui novo ID (aditivo) -> bump MINOR
  - renomear   : muda o rotulo/descricao de um ID -> bump PATCH
  - deprecar   : marca ID como obsoleto (nunca apaga) -> bump MAJOR se em uso
  - listar     : mostra o conteudo de um arquivo canonico

NUNCA apaga nem reutiliza IDs. Atualiza VERSION e CHANGELOG automaticamente.

Uso:
  python curar.py listar riscos
  python curar.py adicionar riscos --id R0.U.21 --nome "Risco de IA" --campos categoria_basileia=operacional grupo=operacional descricao="Risco de uso de IA"
  python curar.py renomear riscos --id R0.U.21 --nome "Risco de Inteligencia Artificial"
  python curar.py deprecar riscos --id R0.U.21 --substituido_por R0.U.6
  python curar.py adicionar areas --id ORG.TEC.OPF --nome "Open Finance" --campos dominio_id=ORG.TEC descricao="Integracao Open Finance"

Depois de curar, rode: python validar.py
"""
import csv, os, sys, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))

ARQS = {
    "dominios":   "B_ORG_dominios.csv",
    "areas":      "B_ORG_areas.csv",
    "riscos":     "B6_riscos_canonico.csv",
    "disciplinas":"B9_disciplinas_canonico.csv",
}

def _ler(arq):
    caminho = os.path.join(AQUI, arq)
    with open(caminho, encoding="utf-8") as f:
        r = list(csv.reader(f, delimiter=";"))
    return r[0], r[1:]

def _escrever(arq, header, linhas):
    caminho = os.path.join(AQUI, arq)
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(header)
        w.writerows(linhas)

def _versao():
    p = os.path.join(AQUI, "VERSION")
    return open(p).read().strip() if os.path.exists(p) else "1.0.0"

def _set_versao(v):
    open(os.path.join(AQUI, "VERSION"), "w").write(v + "\n")

def _bump(tipo):
    maj, mi, pa = (int(x) for x in _versao().split("."))
    if tipo == "MAJOR": maj, mi, pa = maj+1, 0, 0
    elif tipo == "MINOR": mi, pa = mi+1, 0
    else: pa += 1
    nova = f"{maj}.{mi}.{pa}"
    _set_versao(nova)
    return nova

def _changelog(versao, tipo, msg):
    p = os.path.join(AQUI, "CHANGELOG.md")
    txt = open(p, encoding="utf-8").read() if os.path.exists(p) else "# Changelog do Canonico BooX\n"
    hoje = datetime.date.today().isoformat()
    entrada = f"\n## [{versao}] — {hoje} ({tipo})\n\n- {msg}\n"
    # insere logo apos o cabecalho/intro (antes da primeira entrada de versao)
    idx = txt.find("\n## [")
    if idx == -1:
        txt = txt.rstrip() + "\n" + entrada
    else:
        txt = txt[:idx] + entrada + txt[idx:]
    open(p, "w", encoding="utf-8").write(txt)

def _idx(header, col):
    return header.index(col) if col in header else -1

def _todos_ids(header, linhas):
    i = _idx(header, "id")
    return {l[i] for l in linhas}

def adicionar(dom, novo_id, nome, campos):
    arq = ARQS[dom]; header, linhas = _ler(arq)
    if novo_id in _todos_ids(header, linhas):
        print(f"ERRO: ID '{novo_id}' ja existe (ativo ou deprecado). IDs nunca se reutilizam."); sys.exit(1)
    linha = [""] * len(header)
    linha[_idx(header, "id")] = novo_id
    if _idx(header, "nome") >= 0 and nome: linha[_idx(header, "nome")] = nome
    if _idx(header, "codigo") >= 0: linha[_idx(header, "codigo")] = novo_id
    for k, v in campos.items():
        ci = _idx(header, k)
        if ci < 0:
            print(f"AVISO: campo '{k}' nao existe em {arq}, ignorado."); continue
        linha[ci] = v
    if _idx(header, "status") >= 0: linha[_idx(header, "status")] = "ativo"
    linhas.append(linha)
    _escrever(arq, header, linhas)
    v = _bump("MINOR")
    _changelog(v, "MINOR", f"Adicionado {dom}: {novo_id} — {nome}")
    print(f"OK: {novo_id} adicionado a {dom}. Canonico agora v{v}.")
    print("Rode: python validar.py")

def renomear(dom, alvo_id, nome=None, descricao=None):
    arq = ARQS[dom]; header, linhas = _ler(arq)
    ii = _idx(header, "id"); achou = False
    for l in linhas:
        if l[ii] == alvo_id:
            achou = True
            if nome and _idx(header,"nome")>=0: l[_idx(header,"nome")] = nome
            if descricao and _idx(header,"descricao")>=0: l[_idx(header,"descricao")] = descricao
    if not achou:
        print(f"ERRO: ID '{alvo_id}' nao encontrado."); sys.exit(1)
    _escrever(arq, header, linhas)
    v = _bump("PATCH")
    _changelog(v, "PATCH", f"Renomeado/editado {dom}: {alvo_id}")
    print(f"OK: {alvo_id} atualizado. Canonico agora v{v}.")

def deprecar(dom, alvo_id, substituido_por=""):
    arq = ARQS[dom]; header, linhas = _ler(arq)
    ii = _idx(header, "id"); si = _idx(header, "status"); spi = _idx(header, "substituido_por")
    if si < 0:
        print(f"ERRO: {arq} nao tem campo status."); sys.exit(1)
    ids = _todos_ids(header, linhas)
    if substituido_por and substituido_por not in ids:
        print(f"ERRO: substituto '{substituido_por}' nao existe em {dom}."); sys.exit(1)
    achou = False
    for l in linhas:
        if l[ii] == alvo_id:
            achou = True
            l[si] = "deprecado"
            if spi >= 0: l[spi] = substituido_por
    if not achou:
        print(f"ERRO: ID '{alvo_id}' nao encontrado."); sys.exit(1)
    _escrever(arq, header, linhas)
    v = _bump("MAJOR")
    msg = f"Deprecado {dom}: {alvo_id}" + (f" (substituido por {substituido_por})" if substituido_por else "")
    _changelog(v, "MAJOR", msg)
    print(f"OK: {alvo_id} marcado como deprecado (nao apagado). Canonico agora v{v}.")
    print("De-paras que usam este ID continuam validos, mas geram aviso de migracao.")

def listar(dom):
    arq = ARQS[dom]; header, linhas = _ler(arq)
    ii = _idx(header,"id"); ni = _idx(header,"nome"); si = _idx(header,"status")
    print(f"{arq} — {len(linhas)} registros (canonico v{_versao()})\n")
    for l in linhas:
        st = l[si] if si>=0 and si<len(l) else ""
        marca = "" if st=="ativo" else f"  [{st.upper()}]"
        nome = l[ni] if ni>=0 else ""
        print(f"  {l[ii]:18s} {nome}{marca}")

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    acao = sys.argv[1]
    def getarg(flag, default=None):
        return sys.argv[sys.argv.index(flag)+1] if flag in sys.argv else default
    def getcampos():
        if "--campos" not in sys.argv: return {}
        out={}
        for tok in sys.argv[sys.argv.index("--campos")+1:]:
            if tok.startswith("--"): break
            if "=" in tok:
                k,v=tok.split("=",1); out[k]=v
        return out

    if acao == "listar":
        listar(sys.argv[2])
    elif acao == "adicionar":
        adicionar(sys.argv[2], getarg("--id"), getarg("--nome",""), getcampos())
    elif acao == "renomear":
        renomear(sys.argv[2], getarg("--id"), getarg("--nome"), getarg("--descricao"))
    elif acao == "deprecar":
        deprecar(sys.argv[2], getarg("--id"), getarg("--substituido_por",""))
    else:
        print(f"Acao desconhecida: {acao}"); print(__doc__)

if __name__ == "__main__":
    main()
