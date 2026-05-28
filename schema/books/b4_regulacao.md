# B4 — Regulação e Circulares

Regulação externa aplicável ao banco: leis, resoluções CMN, resoluções e
circulares BCB, instruções CVM, normas SUSEP, autorregulação ANBIMA. Pode
ser populado a partir do catálogo público do ChassiRO ou mantido pela casa.

## Arquivos

Este Book tem **dois arquivos**:

1. `B4_regulacao.csv` — as normas
2. `B4_vinculo_norma.csv` — vínculos da norma a processos e riscos

## Arquivo 1: `B4_regulacao.csv`

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | string | sim | ID da norma (ex: `RES_CMN_4557`) |
| `tipo` | string | sim | Tipo: `lei`, `res_cmn`, `res_bcb`, `circ_bcb`, `inst_cvm`, `res_susep`, `anbima`, ... |
| `numero` | string | sim | Número da norma |
| `ano` | inteiro | não | Ano de publicação |
| `regulador` | string | sim | Regulador emissor (CMN, BCB, CVM, SUSEP, ANBIMA, ...) |
| `titulo` | string | não | Título da norma |
| `ementa` | string | não | Ementa / resumo |
| `status` | enum | sim | `vigente`, `revogada`, `futura` |
| `url_oficial` | string | não | Link para o texto oficial |

## Arquivo 2: `B4_vinculo_norma.csv`

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | inteiro | sim | ID do vínculo |
| `norma_id` | string | sim | Norma (ref. B4) |
| `alvo_tipo` | enum | sim | `processo` ou `risco` |
| `alvo_id` | string | sim | ID do processo (B1) ou risco (B6) |
| `tipo_vinculo` | enum | não | `primaria`, `secundaria`, `informativa` |
| `notas` | string | não | Observações |

## Validações

- `id` único em cada arquivo
- `status` ∈ {vigente, revogada, futura}
- No vínculo: `norma_id` existe em B4; `alvo_id` existe em B1 (se processo) ou B6 (se risco)
- `alvo_tipo` ∈ {processo, risco}

## Papel no BooX Lite

Na versão Lite, B4 é usado para **contexto e rastreabilidade**: cada par
processo × risco pode ser associado às normas que o regem, enriquecendo o
parecer ("este risco é regido por X normas"). Não altera diretamente o
cálculo do score X nesta versão — mas a presença de apontamento de
regulador (B2) sobre um processo regido por norma específica torna o
parecer mais preciso.

## Relacionamentos

- Vínculos apontam para **B1** (processos) e **B6** (riscos)

## Exemplo

`B4_regulacao.csv`:
```csv
id;tipo;numero;ano;regulador;titulo;ementa;status;url_oficial
RES_CMN_4557;res_cmn;4557;2017;CMN;Estrutura de gerenciamento de riscos;Dispoe sobre gerenciamento de riscos e de capital;vigente;https://www.bcb.gov.br/...
RES_BCB_265;res_bcb;265;2022;BCB;Gerenciamento de risco operacional;Estrutura de gerenciamento continuo de risco operacional;vigente;https://www.bcb.gov.br/...
```

`B4_vinculo_norma.csv`:
```csv
id;norma_id;alvo_tipo;alvo_id;tipo_vinculo;notas
1;RES_CMN_4557;risco;R0.U.4;primaria;Estrutura de risco operacional
2;RES_BCB_265;processo;P0.U;primaria;Gerenciamento continuo
```
