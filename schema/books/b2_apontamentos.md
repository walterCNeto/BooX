# B2 — Apontamentos

Todos os apontamentos gerados no banco, de qualquer fonte: controles
internos, auditoria interna, compliance, gestão, e apontamentos de
reguladores. É um dos principais insumos do score de ambiente de controles
(eixo X).

## Arquivo

`B2_apontamentos.csv`

## Colunas

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | string | sim | ID único do apontamento |
| `titulo` | string | sim | Título curto do apontamento |
| `descricao` | string | não | Descrição do que foi apontado |
| `origem` | enum | sim | Fonte: `controles_internos`, `auditoria`, `compliance`, `gestao`, `regulador` |
| `severidade` | enum | sim | `critico`, `alto`, `medio`, `baixo` |
| `status` | enum | sim | `aberto`, `em_tratamento`, `fechado`, `vencido` |
| `processo_id` | string | não | Processo apontado (ref. B1) |
| `risco_id` | string | não | Risco relacionado (ref. B6) |
| `controle_id` | string | não | Controle relacionado (ref. B5) |
| `data_abertura` | data | sim | Data de criação (ISO 8601) |
| `data_prazo` | data | não | Prazo de remediação |
| `data_fechamento` | data | não | Data de fechamento (se fechado) |
| `responsavel` | string | não | Responsável pela remediação (ref. B12 ou livre) |

## Validações

- `id` único
- `origem` ∈ {controles_internos, auditoria, compliance, gestao, regulador}
- `severidade` ∈ {critico, alto, medio, baixo}
- `status` ∈ {aberto, em_tratamento, fechado, vencido}
- `processo_id`, se preenchido, deve existir em B1
- `risco_id`, se preenchido, deve existir em B6
- `controle_id`, se preenchido, deve existir em B5
- `data_fechamento` obrigatória se `status = fechado`
- `data_prazo < hoje` com status diferente de fechado sugere `vencido`

## Como entra no score X

Apontamentos **abertos, em tratamento ou vencidos** contribuem para o score
de ambiente de controles do par processo × risco que referenciam. Fechados
não contribuem (mas ficam no histórico).

Pesos por severidade e origem (parâmetros em `docs/metodologia.md`):

| Fator | Peso base |
|-------|-----------|
| Apontamento aberto (médio) | 1.0 |
| Apontamento alto | 2.0 |
| Apontamento crítico | 4.0 |
| Apontamento de **regulador** | peso × 2 (dobra) |
| Apontamento **vencido** | + 1.5 adicional |

Um apontamento sem `processo_id` nem `risco_id` é registrado mas não
contribui para nenhum par específico — entra apenas em estatísticas
globais do painel.

## Relacionamentos

- `processo_id` → **B1**
- `risco_id` → **B6**
- `controle_id` → **B5**
- `responsavel` → **B12** (opcional)

## Exemplo

```csv
id;titulo;descricao;origem;severidade;status;processo_id;risco_id;controle_id;data_abertura;data_prazo;data_fechamento;responsavel
AP-2025-0042;Log de acesso incompleto;Trilha de auditoria nao cobre acessos privilegiados;auditoria;alto;aberto;P2.U.8.1;R0.U.5;CTRL-CYBER-003;2025-11-15;2026-03-31;;Ciberseguranca
AP-2025-0051;Falta segregacao no comite;Aprovador tambem origina;controles_internos;critico;em_tratamento;P2.B.2.1;R0.U.7;CTRL-CRED-002;2025-12-01;2026-02-28;;Credito PJ
AP-2026-0003;Determinacao BACEN sobre PLD;Reforco de monitoramento exigido;regulador;alto;aberto;P2.U.8.2;R0.U.8;;2026-01-20;2026-04-30;;Compliance
```
