# B1 — Processos

Todos os processos do banco, em qualquer nível da hierarquia. É um dos dois
eixos estruturais do BooX (o outro é B6 Riscos).

## Hierarquia

Processos seguem uma hierarquia de até 5 níveis: **P0 → P1 → P2 → P3 → P4**.

- **P0** — Núcleo de processo (ex: P0.B = processos bancários)
- **P1** — Macroprocesso (ex: P1.B.2 = concessão de crédito)
- **P2** — Processo (ex: P2.B.2.1 = análise de crédito PJ)
- **P3** — Subprocesso
- **P4** — Atividade

Os núcleos seguem a convenção do catálogo de controles:
`U` (universal), `B` (bancário), `MC` (mercado de capitais), `S` (seguros),
`P` (previdência), `C` (consórcio), `CG` (conglomerado).

## Arquivo

`B1_processos.csv`

## Colunas

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | string | sim | ID único do processo (ex: `P2.B.2.1`) |
| `codigo` | string | sim | Código legível (pode coincidir com id) |
| `nome` | string | sim | Nome do processo |
| `nivel` | inteiro | sim | Nível hierárquico (0 a 4) |
| `nucleo` | string | sim | Núcleo (U, B, MC, S, P, C, CG) |
| `parent_id` | string | não | ID do processo pai (vazio para P0) |
| `descricao` | string | não | Descrição do que o processo faz |
| `owner_area` | string | não | Área responsável (livre ou ref. B12) |
| `entrada` | string | não | Inputs do processo (texto ou lista com `|`) |
| `saida` | string | não | Outputs do processo (texto ou lista com `|`) |
| `criticidade_bia` | inteiro | não | Criticidade BIA 1-5, se mapeada |

## Validações

- `id` único em todo o Book
- `nivel` coerente com o `id` (P2.x.y.z deve ter nivel=2)
- `parent_id`, se preenchido, deve existir como `id` de outro processo
- `nucleo` ∈ {U, B, MC, S, P, C, CG}
- P0 não tem `parent_id`; P1-P4 devem ter

## Relacionamentos

- Referenciado por **B2** (apontamentos apontam processos)
- Referenciado por **B5** (controles operam em processos)
- Referenciado por **B6** (vínculo processo × risco)
- Referenciado por **B7** (visões filtram processos)
- Referenciado por **B8** (sinais externos podem apontar processos)

## Exemplo

```csv
id;codigo;nome;nivel;nucleo;parent_id;descricao;owner_area;entrada;saida;criticidade_bia
P0.B;P0.B;Processos Bancarios;0;B;;Nucleo de processos bancarios;;;;
P1.B.2;P1.B.2;Concessao de Credito;1;B;P0.B;Macroprocesso de concessao;Credito;Proposta de credito;Operacao contratada;5
P2.B.2.1;P2.B.2.1;Analise de Credito PJ;2;B;P1.B.2;Analise e decisao PJ;Credito PJ;Dossie PJ|SCR|Balanco;Parecer de credito;5
```

## Notas

- A criticidade BIA, quando presente, é um **sinal indireto de impacto**
  que pode reforçar o eixo Y de riscos vinculados a este processo.
- `entrada` e `saida` capturam o IPSO (Inputs / Processamento / Saídas)
  de forma simplificada nesta versão Lite. Versões futuras detalham mais.
