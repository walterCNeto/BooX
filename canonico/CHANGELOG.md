# Changelog do Canonico BooX

Versionamento semantico do vocabulario canonico.

- **PATCH** (x.y.Z): correcao de rotulo ou descricao de um ID existente.
- **MINOR** (x.Y.0): adicao de novos IDs (aditivo, nao quebra de-paras).
- **MAJOR** (X.0.0): deprecacao de IDs em uso ou mudanca incompativel.

## [1.2.0] — 2026-11-17 (MINOR)

- Adicionados 45 testes `TST.CMN4968.001-045` (RES_CMN_4968, arts. 4 a 10), todos `proposto`.
- Fonte: texto vigente da Res. CMN 4.968/2021 (BCB, atualizado em 29/12/2025). Alinea revogada em 1/1/2026 (art. 5, IV, "i", Res. Conjunta 18/2025) nao incluida.
- Aplicabilidade: exclui corretora, dtvm, distribuidora, consorcio e instituicao_pagamento (art. 1, par. unico, Res. CMN 5.117/2024). Inclusao de cooperativa e fintech_credito e interpretacao a validar.
- Campos metodo, evidencia, frequencia, criticidade e controle esperado sao interpretacao; descricao e artigo seguem o texto.

## [1.1.1] — 2026-05-28 (PATCH)

- Renomeado/editado riscos: R0.U.21

## [1.1.0] — 2026-05-28 (MINOR)

- Adicionado riscos: R0.U.21 — Risco de IA Generativa

## [1.0.0] — 2026-05-28

### Inicial
- 13 dominios organizacionais (B_ORG_dominios)
- 73 areas funcionais (B_ORG_areas)
- 20 riscos R0 (B6_riscos_canonico), ancorados no Pilar 3
- 21 disciplinas (B9_disciplinas_canonico)
- Campos de governanca adicionados: status (ativo/deprecado) e substituido_por
