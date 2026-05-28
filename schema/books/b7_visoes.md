# B7 — Visões

As Visões são os **recortes** que o banco quer enxergar: visão produto
(ex: Consignado INSS), visão processo (ex: Crédito), visão ponta-a-ponta
(E2E), visão por disciplina, por segmento. Uma Visão é uma configuração
persistida de filtros que, ao ser executada, gera um 20-box próprio.

## Visão como cidadão de primeira classe

No BooX, Visão **não é filtro ad-hoc** — é objeto registrado, com nome,
owner e filtros definidos. Isso permite:

- Recalcular a mesma Visão a cada ciclo (série temporal por Visão)
- Comparar "Consignado INSS Q1" vs "Consignado INSS Q2"
- Padronizar o que o comitê olha (todos veem a mesma Visão)

## Arquivos

Este Book tem **dois arquivos**:

1. `B7_visoes.csv` — definição das visões
2. `B7_visao_filtros.csv` — os filtros de cada visão

## Arquivo 1: `B7_visoes.csv`

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | string | sim | ID único da visão (ex: `VIS_CONSIGNADO_INSS`) |
| `nome` | string | sim | Nome legível |
| `tipo` | enum | sim | `produto`, `processo`, `e2e`, `disciplina`, `segmento`, `area`, `livre` |
| `descricao` | string | não | O que esta visão mostra e por quê |
| `owner` | string | não | Quem mantém esta visão (ref. B12 ou livre) |
| `regra_afetacao` | enum | não | Para visão por área: `afetada` (default) ou `gestora` |

## Arquivo 2: `B7_visao_filtros.csv`

Cada linha é um critério de filtro. Múltiplas linhas com o mesmo
`visao_id` são combinadas (lógica OR dentro do mesmo `dimensao`, AND entre
dimensões diferentes).

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `visao_id` | string | sim | Visão (ref. B7_visoes) |
| `dimensao` | enum | sim | `processo`, `risco`, `disciplina`, `segmento`, `nucleo`, `categoria_basileia`, `area` |
| `operador` | enum | sim | `igual`, `prefixo`, `em`, `descendente_de` |
| `valor` | string | sim | Valor do filtro (ID ou lista com `|`) |

## Operadores de filtro

| operador | significado | exemplo |
|----------|-------------|---------|
| `igual` | match exato | `dimensao=disciplina, valor=DISC_CREDITO` |
| `prefixo` | ID começa com | `dimensao=processo, valor=P1.B.2` |
| `em` | está na lista | `dimensao=risco, valor=R0.U.5\|R0.U.6` |
| `descendente_de` | é filho (recursivo) de | `dimensao=processo, valor=P0.B` |

## Validações

- `id` único em `B7_visoes.csv`
- `tipo` ∈ enum
- `regra_afetacao` ∈ {afetada, gestora} quando preenchido
- No filtro: `visao_id` existe; `dimensao` e `operador` ∈ enums
- `valor` deve resolver para registros existentes (aviso se vazio)

## Como a Visão gera o 20-box

1. O BooX parte de **todos os pares** processo × risco (B6 vínculo)
2. Aplica os filtros da Visão para selecionar o subconjunto relevante
3. Para visão por **área** com `regra_afetacao=afetada`: inclui apenas
   pares onde a área consta em `area_afetada` (ver B6)
4. Calcula score X e Y de cada par selecionado
5. Plota no 20-box; gera parecer e detalhamento daquele recorte

## Relacionamentos

- Filtros referenciam **B1** (processo), **B6** (risco), **B9** (disciplina), **B13** (segmento)
- `owner` → **B12** (opcional)

## Exemplo

`B7_visoes.csv`:
```csv
id;nome;tipo;descricao;owner;regra_afetacao
VIS_CONSIGNADO_INSS;Consignado INSS;produto;Risco do produto consignado INSS ponta a ponta;Credito PF;
VIS_CYBER_LGPD;Cyber e LGPD;disciplina;Riscos de seguranca da informacao e privacidade;Ciberseguranca;
VIS_CREDITO_E2E;Credito End-to-End;e2e;Todo o ciclo de credito;Credito;
```

`B7_visao_filtros.csv`:
```csv
visao_id;dimensao;operador;valor
VIS_CONSIGNADO_INSS;processo;descendente_de;P1.B.2
VIS_CONSIGNADO_INSS;segmento;igual;SEG_CONSIGNADO
VIS_CYBER_LGPD;disciplina;em;DISC_CYBER|DISC_LGPD
VIS_CREDITO_E2E;disciplina;igual;DISC_CREDITO
```
