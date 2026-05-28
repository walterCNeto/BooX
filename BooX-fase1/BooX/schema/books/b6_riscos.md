# B6 — Riscos

Todos os riscos do banco, com taxonomia hierárquica. É o segundo eixo
estrutural do BooX. Inclui também o **vínculo processo × risco**, que é a
unidade de avaliação do 20-box.

## Hierarquia

Riscos seguem uma hierarquia de até 5 níveis: **R0 → R1 → R2 → R3 → R4**.

- **R0** — Grande tema de risco (ex: R0.U.5 = Risco Cibernético)
- **R1** — Risco (ex: R1.U.5.1 = Vazamento de credenciais)
- **R2 a R4** — Sub-riscos progressivamente granulares

Mesma convenção de núcleos do B1 (U, B, MC, S, P, C, CG).

## Arquivos

Este Book tem **dois arquivos**:

1. `B6_riscos.csv` — a taxonomia de riscos
2. `B6_vinculo_processo_risco.csv` — quais riscos existem em quais processos

## Arquivo 1: `B6_riscos.csv`

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | string | sim | ID único do risco (ex: `R0.U.5`) |
| `codigo` | string | sim | Código legível |
| `nome` | string | sim | Nome do risco |
| `nivel` | inteiro | sim | Nível hierárquico (0 a 4) |
| `nucleo` | string | sim | Núcleo (U, B, MC, S, P, C, CG) |
| `parent_id` | string | não | ID do risco pai (vazio para R0) |
| `descricao` | string | não | Descrição do risco |
| `categoria_basileia` | string | não | Categoria Basileia II (credito, mercado, operacional, ...) |
| `disciplina_id` | string | não | Disciplina associada (ref. B9) |

## Arquivo 2: `B6_vinculo_processo_risco.csv`

Esta é a tabela central do BooX — **cada linha é um par avaliável**.

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | inteiro | sim | ID único do vínculo |
| `processo_id` | string | sim | ID do processo (ref. B1) |
| `risco_id` | string | sim | ID do risco (ref. B6) |
| `materialidade_inerente` | inteiro | sim | Impacto inerente 1-5 (eixo Y) |
| `materialidade_declarada_por` | string | não | Quem declarou (ex: CRO, area) |
| `area_afetada` | string | não | Áreas afetadas, lista com `|` (ref. B12 ou livre) |
| `area_gestora` | string | não | Área gestora do controle (ref. B12 ou livre) |
| `eh_gestora_e_afetada` | bool | não | A área dona é afetada E gestora? |
| `notas` | string | não | Observações sobre o vínculo |

## Validações

- `id` único em cada arquivo
- `nivel` coerente com o `id`
- `parent_id`, se preenchido, deve existir
- No vínculo: `processo_id` deve existir em B1, `risco_id` em B6
- `materialidade_inerente` ∈ {1, 2, 3, 4, 5}
- `categoria_basileia`, se preenchida, valor reconhecido
- `disciplina_id`, se preenchida, deve existir em B9

## Mapeamento materialidade → eixo Y

| materialidade_inerente | Nível de Impacto | score_Y |
|------------------------|------------------|---------|
| 1 | Imaterial | 0.5 |
| 2 | Baixo | 1.5 |
| 3 | Médio | 2.5 |
| 4 | Alto | 3.5 |
| 5 | Elevado | 4.5 |

## Relacionamentos

- `processo_id` → **B1**
- `risco_id` → este Book (B6)
- `disciplina_id` → **B9**
- `area_afetada`, `area_gestora` → **B12** (opcional, livre na versão Lite)
- Apontamentos (**B2**), controles (**B5**), indicadores (**B10**) e
  sinais externos (**B8**) referenciam riscos por `risco_id`

## A distinção afetada × gestora

O BooX captura que um risco pode **afetar** uma área sem que ela seja
**gestora** do controle. Exemplo: o risco cibernético afeta Crédito PJ
(decisões baseadas em dados comprometidos), mas a gestão do controle é de
Cibersegurança.

Para o 20-box **por área**, vale a regra: um risco entra no mapa de uma
área se, e somente se, a **afeta**. Ser gestora é um atributo da relação,
não critério de inclusão. (Esta regra é aplicada nas Visões — ver B7.)

## Exemplo

`B6_riscos.csv`:
```csv
id;codigo;nome;nivel;nucleo;parent_id;descricao;categoria_basileia;disciplina_id
R0.U.5;R0.U.5;Risco Cibernetico;0;U;;Falhas de seguranca da informacao;operacional;DISC_CYBER
R1.U.5.1;R1.U.5.1;Vazamento de credenciais;1;U;R0.U.5;Exposicao de credenciais;operacional;DISC_CYBER
```

`B6_vinculo_processo_risco.csv`:
```csv
id;processo_id;risco_id;materialidade_inerente;materialidade_declarada_por;area_afetada;area_gestora;eh_gestora_e_afetada;notas
1;P2.B.2.1;R0.U.5;4;CRO;Credito PJ;Ciberseguranca;false;Decisao depende de dados integros
2;P2.U.8.1;R0.U.5;5;CRO;Ciberseguranca;Ciberseguranca;true;Operacao propria de SI
```
