# B10 — Indicadores

Indicadores de risco operacional (KRIs) do banco. São metas de redução de
falhas e/ou de perdas — **não** indicadores de estratégia de negócio. Têm
natureza de série temporal e trazem a **dinâmica** ao score (apontamentos
são fotografia; KRIs mostram movimento).

## Arquivos

Este Book tem **dois arquivos**:

1. `B10_indicadores.csv` — definição de cada KRI
2. `B10_indicador_serie.csv` — valores mensais (série temporal)

## Arquivo 1: `B10_indicadores.csv`

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | string | sim | ID único do KRI |
| `nome` | string | sim | Nome do indicador |
| `descricao` | string | não | O que mede |
| `risco_id` | string | não | Risco monitorado (ref. B6) |
| `processo_id` | string | não | Processo monitorado (ref. B1) |
| `disciplina_id` | string | não | Disciplina (ref. B9) |
| `unidade` | string | não | Unidade (%, R$, contagem, dias) |
| `direcao` | enum | sim | `menor_melhor` ou `maior_melhor` |
| `limite_amarelo` | número | não | Limiar de alerta amarelo |
| `limite_vermelho` | número | não | Limiar de alerta vermelho |
| `meta` | número | não | Meta do indicador |

## Arquivo 2: `B10_indicador_serie.csv`

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `indicador_id` | string | sim | ID do KRI (ref. B10_indicadores) |
| `competencia` | string | sim | Mês de referência (`AAAA-MM`) |
| `valor` | número | sim | Valor observado |

## Validações

- `id` único em `B10_indicadores.csv`
- `direcao` ∈ {menor_melhor, maior_melhor}
- `risco_id`, `processo_id`, `disciplina_id`, se preenchidos, existem nos respectivos Books
- Em `B10_indicador_serie.csv`: `indicador_id` deve existir
- `competencia` no formato `AAAA-MM`
- Par (`indicador_id`, `competencia`) único na série

## Status do KRI (derivado)

O BooX deriva o status de cada KRI no período mais recente comparando o
`valor` aos limites, respeitando a `direcao`:

| Status | Condição (direcao = menor_melhor) |
|--------|-----------------------------------|
| verde | valor < limite_amarelo |
| amarelo | limite_amarelo ≤ valor < limite_vermelho |
| vermelho | valor ≥ limite_vermelho |

(Para `maior_melhor`, as comparações se invertem.)

E deriva a **tendência** comparando os últimos meses: `melhora`,
`estavel`, `piora`.

## Como entra no score X

KRIs contribuem para o par (processo, risco) que monitoram:

| Fator | Peso |
|-------|------|
| KRI vermelho | 3.0 |
| KRI amarelo | 1.0 |
| KRI em tendência de piora (6m) | +1.0 adicional |

KRIs trazem antecipação: um indicador piorando, mesmo antes de virar
apontamento, já eleva o score — sinalizando o problema antes que ele se
materialize.

## Relacionamentos

- `risco_id` → **B6**
- `processo_id` → **B1**
- `disciplina_id` → **B9**

## Exemplo

`B10_indicadores.csv`:
```csv
id;nome;descricao;risco_id;processo_id;disciplina_id;unidade;direcao;limite_amarelo;limite_vermelho;meta
KRI-CRED-01;Inadimplencia 90d PJ;Carteira PJ vencida acima 90 dias;R0.U.1;P2.B.2.1;DISC_CREDITO;%;menor_melhor;2.0;4.0;1.5
KRI-CYBER-01;Tentativas de intrusao bloqueadas vs sucesso;Taxa de sucesso de ataques;R0.U.5;P2.U.8.1;DISC_CYBER;%;menor_melhor;0.5;2.0;0.1
```

`B10_indicador_serie.csv`:
```csv
indicador_id;competencia;valor
KRI-CRED-01;2025-07;1.8
KRI-CRED-01;2025-08;2.1
KRI-CRED-01;2025-09;2.4
KRI-CRED-01;2025-10;2.9
KRI-CRED-01;2025-11;3.3
KRI-CRED-01;2025-12;3.8
```

(Neste exemplo, KRI-CRED-01 está amarelo em dezembro e em clara tendência
de piora — 1.8 → 3.8 em seis meses —, o que eleva o score X do par
P2.B.2.1 × R0.U.1.)
