# Changelog do Canonico BooX

Versionamento semantico do vocabulario canonico.

- **PATCH** (x.y.Z): correcao de rotulo ou descricao de um ID existente.
- **MINOR** (x.Y.0): adicao de novos IDs (aditivo, nao quebra de-paras).
- **MAJOR** (X.0.0): deprecacao de IDs em uso ou mudanca incompativel.

## [1.5.0] — 2026-11-17 (MINOR)

- Adicionados 229 testes `proposto` do corpus CVM, ANBIMA e CMN 4.893: TST.CVM030 (19), TST.CVM032 (26), TST.CVM033 (34), TST.CVM161 (22), TST.CVM035 (52), TST.CVM021 (33), TST.ANBSUIT (19) e TST.CMN4893 (24).
- Fonte: textos consolidados anexados pelo usuario (CVM 21, 30, 32, 33, 35 e 161; Regras e Procedimentos de Suitability ANBIMA; CMN 4.893 atualizada em 19/12/2025). Redacoes antigas e vigentes aparecem juntas nos consolidados da CVM: foi usada apenas a redacao vigente (CVM 134/22, 179/23 e 209/24 na Res. 35; 162/22, 167/22, 179/23 e 209/24 na Res. 21; 173/22, 207/24 e 222/24 na Res. 161).
- ANBIMA: o documento recebido e uma versao em revisao (marcas de alteracao e numero de normativo em branco). Conferir a versao publicada antes de validar. O Laudo ANBIMA esta na Secao IV (art. 13), testes TST.ANBSUIT.015-018.
- CMN 4.893: o consolidado inclui a Res. CMN 5.274/2025 (arts. 3 par. 2, 3-A e 22-A, testes de intrusao anuais, MFA, isolamento Pix e STR). Os testes baseados nela estao marcados no campo artigo. Verificar a data de vigencia de cada dispositivo antes de validar.
- Aplicabilidade: CMN 4.893 exclui corretora, dtvm, distribuidora, consorcio e instituicao_pagamento (art. 1, par. unico, Res. CMN 5.117/2024); inclusao de cooperativa e fintech_credito a validar. Normas CVM 21 e 33: gestor_recursos e administrador_fiduciario, mais bancos e DTVMs conforme a atividade. CVM 35, 30 e 161: corretora, dtvm, distribuidora (e bancos em 30 e 161).
- Sobreposicao: Res. CVM 30, 32, 35 e 50 ja sao referenciadas pelos testes PQO (CAD.001-014) e pelas sementes TST.SEED. Ha dupla contagem possivel ate o campo `equivale_a` existir.
- Campos metodo, evidencia, frequencia, criticidade, controle esperado e aplicabilidade sao interpretacao; descricao e artigo seguem o texto oficial.

## [1.4.0] — 2026-11-17 (MINOR)

- Adicionados 71 testes `TST.CIRC3978.001-071` (CIRC_BCB_3978, PLD-FT), todos `proposto`.
- Fonte: texto vigente da Circ. BCB 3.978/2020 com redacoes das Res. BCB 119/2021, 282/2022, 344/2023 e 591/2026 (indicadas no campo `artigo`).
- Aplicabilidade: instituicoes autorizadas pelo BCB (art. 1), exceto seguradora, previdencia, capitalizacao, administrador_fiduciario e gestor_recursos. Recorte por tipo e interpretacao a validar.
- Art. 23-A (dispensa em renegociacao de dividas) e art. 24 par. 3 (excecoes de beneficiario final) tratados dentro dos testes correspondentes, sem teste proprio.
- Frequencia "bienal" nao existe no vocabulario: revisao de dois anos registrada na descricao com frequencia "anual".

## [1.3.0] — 2026-11-17 (MINOR)

- Adicionados 37 testes `TST.CMN4557.001-037` (RES_CMN_4557, arts. 33 a 36 e 56), todos `proposto`.
- Fonte: texto da Res. CMN 4.557/2017 com redacoes da CMN 4.943/2021 e da CMN 5.076/2023 (indicadas no campo `artigo`).
- Art. 32 (definicao de risco operacional) nao gera teste. Art. 56 truncado no texto recebido apos o par. 1, inciso III.
- Aplicabilidade restrita a banco_multiplo e banco_comercial. Enquadramento por segmento (S1 a S5) e atividades de pagamento a validar.

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
