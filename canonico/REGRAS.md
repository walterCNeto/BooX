# Regras de Curadoria do Canonico BooX

O canonico e o **vocabulario comum** do BooX: todo de-para (B_MAP) de todo
banco aponta para IDs canonicos. Por isso ele precisa ser **estavel**, mas
o mundo muda (regulacao, riscos novos, areas novas) — entao ele tambem
precisa **evoluir**. Estas regras conciliam as duas coisas.

## Principio fundamental

> **Aditivo e livre. Destrutivo e proibido. Em vez de apagar, depreca.**

Um ID canonico, uma vez publicado, **nunca e apagado nem reutilizado**.
Todos os de-paras existentes dependem dele. Apagar um ID quebra
silenciosamente o trabalho de quem ja mapeou para ele.

## O que e permitido

| Acao | Permitido? | Efeito na versao |
|------|-----------|------------------|
| **Adicionar** novo ID (risco, area, dominio, disciplina) | Sim, livre | MINOR (x.Y.0) |
| **Renomear o rotulo** (campo `nome`) de um ID | Sim | PATCH (x.y.Z) |
| **Editar a descricao** de um ID | Sim | PATCH (x.y.Z) |
| **Deprecar** um ID (marcar como obsoleto) | Sim, com cautela | MAJOR (X.0.0) se em uso |
| **Apagar** um ID | **Nunca** | — |
| **Reutilizar** um ID antigo para outra coisa | **Nunca** | — |

## Como funciona a deprecacao

Em vez de apagar, um ID que nao serve mais recebe:

- `status = deprecado`
- `substituido_por = <ID novo>` (se houver substituto; vazio se foi apenas
  descontinuado)

O ID deprecado **continua no arquivo**. Os de-paras antigos que apontam
para ele continuam funcionando, mas o BooX emite um aviso na analise de
suficiencia: "este de-para usa ID deprecado X; migre para Y". A migracao e
gradual e nunca silenciosa.

## Regras de formacao de ID

- IDs sao **estaveis e legiveis**, com hierarquia por prefixo:
  - Riscos: `R0.U.N`, sub-riscos `R1.U.N.M`, etc.
  - Organizacao: `ORG.<DOMINIO>` e `ORG.<DOMINIO>.<AREA>`
  - Disciplinas: `DISC_<NOME>`
- Um ID novo nunca colide com um existente (nem ativo, nem deprecado).
- O proximo numero de uma sequencia e sempre **maior** que qualquer ja
  usado (mesmo deprecado) — nunca se reaproveita um "buraco".

## Conceito, nunca marca

Mantida a regra fundadora: o canonico usa apenas **conceitos genericos**,
nunca marcas de banco. "Alta Renda" e canonico; "Personnalite", "Prime",
"Uniclass" sao marcas locais que entram via B_MAP. Toda proposta de adicao
ao canonico passa por esse filtro.

## Quem cura

A curadoria do canonico central e do **mantenedor do projeto**. Mudancas
entram por revisao explicita (ex: pull request no GitHub). Bancos que usam
o BooX nao alteram o canonico central — eles adaptam via B_MAP, e podem
**propor** mudancas ao mantenedor.

## Ferramentas

- `curar.py` — aplica mudancas (adicionar, deprecar, renomear) seguindo
  estas regras automaticamente, com bump de versao e entrada no changelog.
- `validar.py` — checa a integridade do canonico (IDs duplicados,
  `substituido_por` apontando para ID inexistente, hierarquia quebrada).

Toda mudanca no canonico deve passar por `validar.py` antes de ser
publicada.

## Fluxo de uma mudanca

```
1. Identifica necessidade (falta risco X / area Y obsoleta / rotulo errado)
        v
2. Roda curar.py com a acao desejada
   - curar.py adiciona/depreca/renomeia conforme as regras
   - bump automatico de versao (PATCH/MINOR/MAJOR)
   - entrada automatica no CHANGELOG
        v
3. Roda validar.py — confirma integridade
        v
4. Revisa o diff e publica (commit / pull request)
        v
5. Bancos veem a nova versao; de-paras antigos continuam validos;
   IDs deprecados geram aviso de migracao na proxima analise
```
