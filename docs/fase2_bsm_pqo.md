# Fase 2 — Piloto BSM PQO (Roteiro 2025)

Esta e a primeira extracao de **conteudo regulatorio validado** para o
catalogo canonico de testes do BooX. Fonte: **Roteiro do Programa de
Qualificacao Operacional (PQO) da BSM, edicao 2025**, documento publico
distribuido pela B3/BSM aos Participantes do mercado.

URL de referencia:
https://www.bsm.org.br/informacoes-de-autorregulacao/qualificacao-operacional

## Escopo deste piloto

**Apenas o Capitulo 1 — CADASTRAR CLIENTES** (Itens 1 a 14 do Roteiro).

- 14 testes extraidos
- IDs: `TST.BSM.PQO.CAD.001` a `TST.BSM.PQO.CAD.014`
- Status: **`ativo`** (nao mais `proposto`) — primeiros testes do BooX
  com fonte oficial rastreada item-a-item

Capitulos restantes (2-16) ficam como proxima iteracao:

| Cap | Tema | Itens estimados |
|-----|------|-----------------|
| 2 | Suitability | 10 (15-24) |
| 3 | Executar Ordens | ~25 |
| 4 | Liquidar Negocios e Conta Margem | ~15 |
| 5 | Custodia de Ativos e Posicoes | ~20 |
| 6 | Gerenciar Risco | ~15 |
| 7 | Assessor de Investimento | ~10 |
| 8 | Controles Internos | ~30 |
| 9 | PLD | ~15 |
| 10 | Supervisao de Operacoes | ~10 |
| 11 | Certificacao de Profissionais | ~10 |
| 12 | Seguranca da Informacao | ~20 |
| 13 | Continuidade e Mudancas | ~15 |
| 14 | Infraestrutura de TI | ~15 |
| 15 | Prevencao a Fraude | ~10 |
| 16 | Suporte a Infraestrutura | ~10 |

Total estimado quando completo: **~230 testes**.

## Metodologia de extracao

Cada "Item" numerado do Roteiro PQO vira um teste canonico. A estrutura
do PQO facilita: a coluna esquerda ja informa a norma e artigo originarios.

### O que vem do texto literal do PQO (fidelidade a BSM)
- `titulo` — resumo em uma linha do requisito
- `descricao` — enunciado do Item, parafraseado para caber (texto integral
  pode ser consultado no PDF oficial, Item correspondente)
- `norma_id` — codificacao da coluna esquerda do PQO (ex: `RES_CVM_35`)
- `artigo` — artigo/paragrafo citado na coluna esquerda
- `aplicabilidade` — Participantes do PQO: corretora, dtvm, distribuidora

### O que e interpretacao do mantenedor (operacionalizacao)
- `metodo_verificacao` — como auditar o cumprimento (revisao documental,
  teste amostral, observacao, analitico, automatizado)
- `evidencia_esperada` — artefato que comprova o atendimento
- `frequencia_minima` — periodicidade adequada de verificacao
- `criticidade` — severidade em caso de descumprimento (alta/media/baixa)
- `risco_r0_canonico` — risco R0 do BooX mais associado ao requisito
- `controle_esperado_texto` — descricao do controle-alvo

**Nota importante:** o PQO diz "O Participante deve X", nao "para verificar
X, aplique teste Y". Os campos de operacionalizacao sao inferencia tecnica
do mantenedor, uteis para orientar a estrutura de controles do banco, mas
nao vem do texto literal do regulador.

### Codificacao de normas

As normas citadas no PQO sao codificadas com IDs limpos:

| ID BooX | Norma |
|---------|-------|
| `RES_CVM_30` | Resolucao CVM 30/2021 (Suitability) |
| `RES_CVM_32` | Resolucao CVM 32/2021 (Agentes de Custodia) |
| `RES_CVM_35` | Resolucao CVM 35/2021 (Conduta de intermediarios) |
| `RES_CVM_50` | Resolucao CVM 50/2021 (PLD-FT no SMI) |
| `OC_111_2020_PRE` | Oficio Circular 111/2020-PRE (contrato de intermediacao) |
| `OC_048_2017_DP` | Oficio Circular 048/2017-DP (nao residente) |
| `OC_110_2020_PRE` | Oficio Circular 110/2020-PRE (cadastro) |
| `OC_053_2012_DP` | Oficio Circular 053/2012-DP (declaracao do Cliente) |
| `CE_003_2020_PRE` | Comunicado Externo 003/2020-PRE (atualizacao cadastral) |
| `DELIB_CVM_707` | Deliberacao CVM 707 (cadastro eletronico) |

## Mapeamento ao canonico do BooX (R0)

Os 14 testes do Cap 1 cobrem predominantemente:
- **R0.U.11** (Conformidade) — requisitos de contratos, politicas, RPA/NPA
- **R0.U.12** (Conduta) — relacionamento com Cliente, divulgacao
- **R0.U.13** (Lavagem de Dinheiro e FT) — cadastro, atualizacao, PLD/FTP

Nao ha **FR (Fator de Risco) canonico** atribuido nesta fase — a biblioteca
atual de FRs e focada em Cyber, Conformidade governanca e PLD especifico.
Uma proxima iteracao pode expandir os FRs para cobrir cadastro/KYC.

## Como usar

Rodar o gap regulatorio filtrando por `corretora` ou `dtvm`:

```bash
python -m boox.gap_regulatorio examples/banco_modelo_sa --tipo corretora
```

O relatorio agora inclui os 14 testes do Cap 1 do PQO como aplicaveis
e mostra, dentre os que o banco declara executar (B_TESTES_execucao.csv),
quais estao conforme/parcial/nao conforme/sem execucao.

## Proximos passos

1. **Capitulo 2 (Suitability)** — proxima extracao natural (10 itens)
2. **Capitulo 8 (Controles Internos)** — o mais denso do PQO (~30 itens);
   e o que mais interessa para quem estuda o framework de CI
3. **Capitulo 9 (PLD)** — converter os seeds `TST.SEED.PLDFT.*` em testes
   `ativos` do PQO Cap 9, com atribuicao oficial rastreada
4. **Capitulo 12 (Seguranca da Informacao)** — converter seeds de Cyber
   em testes `ativos`
