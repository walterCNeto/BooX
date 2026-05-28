# B8 — Reguladores e Ouvidoria

Sinais externos capturados sobre o banco: procedentes BACEN, reclamações
Procon, registros de Ouvidoria, processos sancionadores CVM, sanções
ANBIMA, mídia adversa, histórico Reclame Aqui. É o que diferencia o BooX
de um RCSA tradicional que só olha para dentro.

## Princípio

Todos os sinais aqui são, idealmente, **públicos** — acessíveis a qualquer
cidadão (rankings BACEN, processos CVM, sanções ANBIMA, notícias). Isso
permite reproduzir a metodologia sem barreira de acesso. Registros internos
de Ouvidoria também entram, mas o desenho privilegia fontes verificáveis.

## Arquivo

`B8_externos.csv`

## Colunas

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | string | sim | ID único do sinal |
| `fonte` | enum | sim | `bacen`, `cvm`, `anbima`, `procon`, `ouvidoria`, `midia`, `reclame_aqui` |
| `tipo` | string | sim | Tipo do sinal (depende da fonte — ver abaixo) |
| `descricao` | string | não | Descrição do sinal |
| `risco_id` | string | não | Risco associado (ref. B6) |
| `processo_id` | string | não | Processo associado (ref. B1) |
| `disciplina_id` | string | não | Disciplina associada (ref. B9) |
| `severidade` | inteiro | não | Severidade 1-5 (para mídia e similares) |
| `quantidade` | número | não | Quantidade (ex: nº de procedentes no período) |
| `status` | string | não | Status (ex: `julgado`, `em_curso` para CVM) |
| `valor_metrica` | número | não | Valor de métrica contínua (ex: nota Reclame Aqui) |
| `valor_anterior` | número | não | Valor anterior (para detectar tendência) |
| `data` | data | sim | Data de referência do sinal |
| `periodo` | string | não | Período de referência (ex: `2025-Q4`) |

## Tipos por fonte

| fonte | tipos típicos |
|-------|---------------|
| `bacen` | `procedente`, `ranking_reclamacoes` |
| `cvm` | `processo_julgado`, `processo_em_curso` |
| `anbima` | `carta_recomendacao`, `termo_compromisso`, `julgamento` |
| `procon` | `procedente` |
| `ouvidoria` | `reclamacao_procedente` |
| `midia` | `noticia_adversa` |
| `reclame_aqui` | `nota_periodo` |

## Validações

- `id` único
- `fonte` ∈ enum
- `risco_id`, se preenchido, existe em B6
- `processo_id`, se preenchido, existe em B1
- `disciplina_id`, se preenchido, existe em B9
- `severidade` ∈ [1, 5] quando preenchida

## Como entra no score X

Cada fonte contribui com peso próprio, com teto (cap), para o par
(processo, risco) ou para todos os pares de uma disciplina:

| Fonte / tipo | Peso | Cap |
|--------------|------|-----|
| BACEN procedente | 0.5 cada | 6.0 |
| BACEN tendência de piora | +1.5 | — |
| CVM processo julgado | 2.0 cada | 6.0 |
| CVM processo em curso | 1.0 cada | 6.0 |
| ANBIMA carta de recomendação | 0.3 cada | 3.0 |
| ANBIMA termo de compromisso | 0.5 cada | 3.0 |
| ANBIMA julgamento | 1.5 cada | 3.0 |
| Procon procedente | 0.3 cada | 3.0 |
| Mídia adversa (severidade ≥ 4) | 1.0 cada | 4.0 |
| Mídia adversa (severidade 3) | 0.4 cada | 4.0 |
| Reclame Aqui (queda ≥ 0.5 na nota) | até 2.0 | — |

CVM tem peso maior porque é regulador estatal com poder sancionador.
ANBIMA é autorregulador (peso médio). Pesos detalhados e ajustáveis em
`docs/metodologia.md`.

## Vínculo dos sinais aos pares

Um sinal pode estar ligado a:

- **Um par específico** (`risco_id` + `processo_id`): contribui só para ele
- **Um risco em todos os processos** (`risco_id` só): contribui para todos os pares daquele risco
- **Uma disciplina** (`disciplina_id`): contribui para todos os pares de riscos daquela disciplina
- **Nada específico**: entra só nas estatísticas globais do painel

## Relacionamentos

- `risco_id` → **B6**
- `processo_id` → **B1**
- `disciplina_id` → **B9**

## Exemplo

```csv
id;fonte;tipo;descricao;risco_id;processo_id;disciplina_id;severidade;quantidade;status;valor_metrica;valor_anterior;data;periodo
EXT-0001;bacen;procedente;Procedentes sobre cobranca indevida;R0.U.7;;DISC_CONDUTA;;16;;;;2025-12-31;2025-Q4
EXT-0002;cvm;processo_julgado;PAS sobre suitability;R0.MC.1;;DISC_CONDUTA;;2;julgado;;;2025-11-20;2025-Q4
EXT-0003;reclame_aqui;nota_periodo;Nota geral caiu;;;;;;;6.5;7.2;2025-12-31;2025-Q4
EXT-0004;midia;noticia_adversa;Reportagem sobre vazamento;R0.U.5;;DISC_CYBER;4;1;;;;2025-10-15;2025-Q4
```
