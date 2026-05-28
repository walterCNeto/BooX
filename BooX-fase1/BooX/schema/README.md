# BooX — Especificação dos Books (v0.1, Lite)

Este documento define os **Books** do BooX: o que cada um contém, suas
colunas, validações e como se relacionam. Esta é a versão **Lite**, com os
9 Books necessários para gerar o 20-box.

Cada Book tem uma página própria em [`books/`](books/).

## Princípios de design

1. **Cada Book é uma tabela.** Uma linha = um registro. Colunas tipadas.
   Formato de troca: CSV (UTF-8) ou Excel. A fonte da verdade pode ser
   qualquer um dos dois.

2. **Books se conectam por chaves.** Um apontamento (B2) referencia um
   processo (B1), um controle (B5) e um risco (B6) por seus IDs. As chaves
   são sempre o campo `id` do Book de destino.

3. **IDs são estáveis e legíveis.** Use IDs canônicos quando existirem
   (`R0.U.5`, `P0.B.2`), ou IDs internos consistentes (`CTRL-CRED-001`).
   Nunca reaproveite um ID para um registro diferente.

4. **Vazio é informação.** Um campo opcional vazio é um estado válido
   ("ainda não avaliado", "não se aplica"). O BooX trata vazio
   explicitamente — não assume valores default silenciosos.

5. **Adicionar Books não quebra nada.** Os 4 Books fora do Lite (B3, B11,
   B12, B13) enriquecem a análise quando presentes, mas a ausência deles
   não impede o cálculo do 20-box.

## A unidade de avaliação: par processo × risco

O BooX avalia cada **par (processo, risco)** de forma independente. Um
risco que aparece em três processos gera três avaliações distintas, porque
o ambiente de controles daquele risco pode ser diferente em cada processo.

Os vínculos processo × risco vivem no Book **B6 (Riscos)** através de uma
tabela de vínculo, ou em um arquivo de vínculos dedicado (ver B6).

## Os dois eixos do 20-box

### Eixo Y — Impacto

Materialidade inerente do risco no processo. Cinco níveis:

| Nível | Faixa de score Y | Significado |
|-------|------------------|-------------|
| Imaterial | [0, 1.0) | Impacto desprezível |
| Baixo | [1.0, 2.0) | Impacto limitado |
| Médio | [2.0, 3.0) | Impacto relevante |
| Alto | [3.0, 4.0) | Impacto significativo |
| Elevado | [4.0, 5.0] | Impacto severo |

O score Y (escala 0-5) vem da **materialidade declarada** pela casa
(prioritária) ou da materialidade default do vínculo processo × risco.

### Eixo X — Ambiente de Controles

Qualidade do ambiente de controles relativa ao risco. Cinco níveis,
**monotonicamente crescente** (esquerda = pior, direita = melhor):

| Símbolo | Nível | Faixa de score X | Significado |
|---------|-------|------------------|-------------|
| `--` | Crítico | [80, 100] | Ambiente francamente insuficiente |
| `-` | Atenção | [60, 80) | Ambiente abaixo do desejado |
| `0` | Neutro | [40, 60) | Estado intermediário ou inconclusivo |
| `+` | Bom | [20, 40) | Ambiente operando satisfatoriamente |
| `++` | Adequado | [0, 20) | Ambiente plenamente adequado ao risco |

O score X (escala 0-100) é **inverso à qualidade**: score alto significa
muitos sinais negativos (apontamentos, KRIs vermelhos, sinais externos),
logo ambiente crítico. Score baixo significa ambiente adequado.

### A célula: Prioridade de Tratamento

Cada par cai em uma célula do 20-box, classificada em cinco níveis de
**Prioridade de Tratamento** — o que a célula comunica ao CRO:

| Prioridade | Significado | Ação |
|------------|-------------|------|
| **Crítico** | Alta exposição + controles insuficientes | Tratamento imediato, visibilidade no comitê |
| **Alto** | Exposição relevante mal endereçada | Plano de remediação com prazo |
| **Médio** | Risco material com controles parciais | Monitoramento próximo |
| **Baixo** | Risco controlado proporcionalmente | Manutenção do ciclo regular |
| **OK** | Risco imaterial com ambiente adequado | Sem ação requerida |

Mapeamento Impacto × Ambiente → Prioridade:

```
                          Ambiente de Controles
              --        -         0         +        ++
Elevado    CRÍTICO   CRÍTICO   ALTO      MÉDIO     MÉDIO
Alto       CRÍTICO   ALTO      MÉDIO     MÉDIO     BAIXO
Médio      ALTO      MÉDIO     MÉDIO     BAIXO     BAIXO
Baixo      MÉDIO     MÉDIO     BAIXO     BAIXO     OK
Imaterial  BAIXO     BAIXO     OK        OK        OK
```

## O score do ambiente de controles (eixo X)

O score X agrega seis componentes, cada um em escala parcial, somados e
limitados a [0, 100]:

```
score_X = f_apontamentos
        + f_controles
        + f_indicadores
        + f_externos
        + f_cobertura
        - f_credito_validacao
```

| Componente | O que mede | Book fonte |
|------------|------------|------------|
| `f_apontamentos` | Apontamentos abertos, ponderados por severidade e origem | B2 |
| `f_controles` | Déficit de eficácia dos controles (5 − eficácia) | B5 |
| `f_indicadores` | KRIs vermelhos/amarelos e tendência de piora | B10 |
| `f_externos` | Sinais externos: BACEN, CVM, ANBIMA, Procon, mídia | B8 |
| `f_cobertura` | Penalidade por baixa cobertura de avaliação | (derivado) |
| `f_credito_validacao` | Crédito quando há validação independente favorável | B5 |

Os pesos exatos de cada componente estão em
[`../docs/metodologia.md`](../docs/metodologia.md) e são parâmetros
ajustáveis — a casa pode recalibrar conforme seu apetite a risco.

## Formato dos arquivos

- **Encoding**: UTF-8
- **CSV**: separador `;` (ponto-e-vírgula, padrão BR), aspas duplas para
  campos com separador interno
- **Datas**: ISO 8601 (`AAAA-MM-DD`)
- **Decimais**: ponto (`.`) como separador decimal
- **Booleanos**: `true` / `false` (minúsculo) ou `1` / `0`
- **Listas em uma célula**: separadas por `|` (pipe)

## Convenção de nomes de arquivo

```
B1_processos.csv
B2_apontamentos.csv
B4_regulacao.csv
B5_controles.csv
B6_riscos.csv
B6_vinculo_processo_risco.csv
B7_visoes.csv
B7_visao_filtros.csv
B8_externos.csv
B9_disciplinas.csv
B10_indicadores.csv
B10_indicador_serie.csv
```
