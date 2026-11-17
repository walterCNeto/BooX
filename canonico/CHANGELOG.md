# Changelog do Canonico BooX

Versionamento semantico do vocabulario canonico.

- **PATCH** (x.y.Z): correcao de rotulo ou descricao de um ID existente.
- **MINOR** (x.Y.0): adicao de novos IDs (aditivo, nao quebra de-paras).
- **MAJOR** (X.0.0): deprecacao de IDs em uso ou mudanca incompativel.

## 1.11.2 - PATCH
- Promovidos a `ativo` 49 testes revisados pelo responsavel: 21 da Res. CMN 4.557 e 28 da Res. CMN 4.968 (todos de criticidade alta).
- Texto conferido contra a versao consolidada vigente (CMN 4.968 em 29/12/2025); dispositivos revogados do art. 5 da 4.968 (inc. IV 'i' e par. unico, Res. Conjunta 18/2025) nao sao citados por nenhum teste.
- Testes de criticidade media/baixa seguem `proposto`.

## [1.11.1] - 2026-11-17 (PATCH)

- Validacao da Circular BCB 3.978: 48 testes de criticidade alta passam de proposto a ativo, apos conferencia dos numeros e prazos contra o texto consolidado (inclui a Resolucao BCB 591/2026) e revisao de metodo, evidencia, frequencia, criticidade e aplicabilidade pelo validador. Os outros 23 testes da norma, inclusive TST.CIRC3978.026, seguem proposto.
- TST.CIRC3978.056: descricao corrigida para a redacao do art. 49, pars. 1 e 2 (operacoes de 1/10/2026 a 31/12/2026 comunicadas no primeiro dia util de janeiro de 2027).

## [1.11.0] - 2026-11-17 (MINOR)

- B_TESTES_canonico ganha a coluna opcional `tipos_fundo` (lista com `|`, vazia = vale para qualquer tipo), no fim do cabecalho, apos `atividades`. Novo enum `tipo_fundo`: fif, fidc, fii, fip.
- Preenchida por id: TST.CVM175A2.* -> fidc (16); TST.CVM175A3.* -> fii (14); TST.CVM175A4.* -> fip (9); TST.CVM175.029 a 043 (artigos "Anexo I") -> fif (15). Parte Geral (TST.CVM175.001-028) e CVM 21 ficam vazias. O recorte e interpretacao a validar.
- Resolve a limitacao registrada na 1.10.0. `validar.py` rejeita valor fora do enum. `gap_regulatorio.analisar(..., tipos_fundo=None)`: None = todos (numeros inalterados); CLI `--tipos-fundo "a|b"`.

## [1.10.0] - 2026-11-17 (MINOR)

- Adicionados 39 testes proposto dos Anexos II (FIDC, 16), III (FII, 14) e IV (FIP, 9) da Resolucao CVM 175: TST.CVM175A2, A3 e A4. Fonte: textos consolidados anexados pelo usuario. Atividades por teste: administracao_fiduciaria, gestao_recursos ou custodia.
- Limitacao: os testes valem para qualquer gestor ou administrador, mesmo sem fundos daquele tipo; falta a dimensao tipos de fundo administrados. Trechos com redacao antiga e vigente duplicadas no consolidado foram lidos pela vigente. Os artigos 21, 27 e 29 (FIDC e FIP) foram resumidos pelo conteudo visivel e remetem ao texto do artigo para o detalhe.

## [1.9.1] — 2026-11-17 (PATCH)

- Coluna atividades refinada em 30 testes da CVM 21 e CVM 175: gestao_recursos, administracao_fiduciaria e custodia separadas pelo texto de cada artigo; em duvida, mantidas as duas atividades. CVM 35 e CVM 30 mantidas.

## [1.9.0] — 2026-11-17 (MINOR)

- B_TESTES_canonico ganha a coluna opcional `atividades` (lista com `|`, vazia = vale para qualquer atividade), no fim do cabecalho. Novo enum `atividade`: administracao_fiduciaria, gestao_recursos, distribuicao, intermediacao, custodia, escrituracao, consultoria.
- Preenchida por norma_id: RES_CVM_21 e RES_CVM_175 -> gestao_recursos|administracao_fiduciaria; RES_CVM_32 -> custodia; RES_CVM_33 -> escrituracao; RES_CVM_35 -> intermediacao; RES_CVM_30 -> distribuicao|intermediacao|consultoria. Demais normas (inclusive CNSP 416 e testes PQO) ficam vazias. O recorte por atividade e interpretacao a validar.
- `validar.py` rejeita valor de `atividades` fora do enum. `gap_regulatorio.analisar(..., atividades=None)`: None = todas (numeros anteriores inalterados); CLI `--atividades "a|b"`.
- O CSV passou a ser gravado com a coluna nova em todas as linhas; nenhum outro campo mudou.

## [1.8.0] — 2026-11-17 (MINOR)

- Adicionados 25 testes `proposto` da Resolucao CNSP 416/2021 (Sistema de Controles Internos, Estrutura de Gestao de Riscos e Auditoria Interna), TST.CNSP416.001..025, regulador SUSEP, aplicabilidade seguradora, previdencia e capitalizacao. Vigencia inicial 2022-01-03 (art. 46).
- Fonte: texto da Resolucao CNSP 416, de 20 de julho de 2021, anexado pelo usuario (versao original; nao foi verificado se ha alteracoes posteriores). `fonte_url` fica vazio ate conferencia da pagina oficial da Susep.
- Escopo: apenas a CNSP 416. NAO estao catalogados capital de risco, provisoes, subscricao, seguranca cibernetica, PLD e demais normas CNSP e Susep; o catalogo da SUSEP e parcial. Dispensas por segmento (S1 a S4) estao descritas no texto de cada teste, mas o motor ainda nao filtra por segmento. Resseguradores e corretoras de seguros nao tem tipo no enum.

## [1.7.0] — 2026-11-17 (MINOR)

- Adicionados 43 testes `proposto` da Resolucao CVM 175 (fundos de investimento), TST.CVM175.001..043: Parte Geral (divulgacao, material, fato relevante, escrituracao e auditoria, contratacao de terceiros, deveres de administrador e gestor, liquidez e estresse, voto, vedacoes, substituicao de prestador, patrimonio liquido negativo, arquivo) e Anexo Normativo I (FIF: informes a CVM, verificacoes do administrador, taxa de performance, ativos no exterior, concentracao por emissor e modalidade, enquadramento, composicao por tipo, credito privado, margem).
- Fonte: texto consolidado da Resolucao CVM 175 anexado pelo usuario (inclui alteracoes ate as Resolucoes CVM 181, 184, 187, 200 e 206). Redacoes antigas e vigentes aparecem duplicadas no consolidado; foi usada a vigente.
- Escopo: Parte Geral e Anexo I. Anexos II (FIDC), III (FII), IV (FIP) e demais ficam para lote proprio. Limites numericos transcritos do texto oficial; metodo, evidencia, frequencia e criticidade sao interpretacao (todos `proposto`).
- Aplicabilidade igual a da CVM 21 (gestor_recursos, administrador_fiduciario, banco_multiplo, dtvm, distribuidora). Nao ha `equivale_a` neste lote.

## [1.6.1] — 2026-11-17 (PATCH)

- Preenchido `equivale_a` em 3 testes cuja obrigacao e a mesma de um teste PQO ja ativo: TST.CVM035.015 -> TST.BSM.PQO.CAD.001 (art. 21, regras de execucao de ordens), TST.CVM035.007 -> TST.BSM.PQO.CAD.013 (art. 6, par. 3, pessoas autorizadas a emitir ordens) e TST.CVM032.004 -> TST.BSM.PQO.CAD.008 (art. 10, contrato de custodia).
- Vinculos conservadores: sobreposicoes apenas parciais (por exemplo CAD.006 e CVM035.004, CAD.002 e CVM035.016) nao foram ligadas, para nao subcontar obrigacoes. Revisar caso a caso na validacao.

## [1.6.0] — 2026-11-17 (MINOR)

- B_TESTES_canonico ganha 4 colunas opcionais, vazias por padrao: `equivale_a` (ID de outro teste que cobre o mesmo requisito), `vigencia_inicio`, `vigencia_fim` (AAAA-MM-DD) e `revogada_por`. Nenhum teste existente foi alterado; nenhum texto de artigo ou descricao mudou.
- `validar.py`: `equivale_a` deve apontar para ID existente (e diferente do proprio), nao pode formar ciclo; datas de vigencia em AAAA-MM-DD e fim >= inicio.
- `gap_regulatorio`: testes ligados por `equivale_a` contam uma vez (representante = menor ID); testes fora de vigencia saem da contagem e vao para bloco proprio. Os vinculos `equivale_a` entre testes PQO, sementes e CVM ainda precisam ser preenchidos (ver 1.5.0).

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
