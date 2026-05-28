# B5 — Controles

Todos os controles de risco operacional do banco, descritos no conceito
**5W2H** e classificados por tipo. É insumo central do score de ambiente
de controles (eixo X), porque a eficácia dos controles é o que mais
diretamente determina se um risco está bem endereçado.

## O conceito 5W2H

Cada controle responde a sete perguntas. Um controle bem descrito tem todas
as sete preenchidas:

| Letra | Pergunta | Coluna |
|-------|----------|--------|
| **What** | O que é feito? | `acao` |
| **Why** | Por quê? (qual risco mitiga) | `risco_id` |
| **Who** | Quem faz? | `responsavel` |
| **Where** | Onde? (sistema, comitê, fluxo) | `local` |
| **When** | Quando? (frequência) | `frequencia` |
| **How** | Como? (manual/automático + descrição) | `mecanismo` + `como` |
| **How much** | Quanto cobre? | `cobertura_pct` |

## Arquivo

`B5_controles.csv`

## Colunas

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | string | sim | ID único do controle (ex: `CTRL-CRED-002`) |
| `acao` | string | sim | **What**: o que o controle faz |
| `tipo` | enum | sim | `icaap`, `operacional`, `credito`, `cobranca`, `mercado`, `liquidez`, `compliance`, `outro` |
| `risco_id` | string | sim | **Why**: risco mitigado (ref. B6) |
| `processo_id` | string | não | Processo onde opera (ref. B1) |
| `responsavel` | string | não | **Who**: papel/área responsável (ref. B12 ou livre) |
| `local` | string | não | **Where**: sistema, comitê, planilha, fluxo |
| `frequencia` | enum | não | **When**: `continuo`, `diario`, `semanal`, `mensal`, `trimestral`, `semestral`, `anual`, `por_evento`, `sob_demanda` |
| `mecanismo` | enum | não | **How**: `manual`, `semi`, `automatico` |
| `como` | string | não | **How**: descrição da operação |
| `cobertura_pct` | número | não | **How much**: % de operações cobertas (0-100) |
| `natureza` | enum | não | `preventivo`, `detectivo`, `corretivo` |
| `eficacia_autoavaliada` | número | não | Eficácia 1-5 declarada pela área (camada 2) |
| `eficacia_validada` | número | não | Eficácia 1-5 validada pela 2ª linha (camada 3) |
| `status_validacao` | enum | não | `apenas_autoavaliado`, `validado_documentalmente`, `validado_amostral`, `validado_completo` |

## Validações

- `id` único
- `risco_id` deve existir em B6
- `processo_id`, se preenchido, deve existir em B1
- `tipo` ∈ valores do enum
- `frequencia`, `mecanismo`, `natureza`, `status_validacao` ∈ enums quando preenchidos
- `eficacia_autoavaliada` e `eficacia_validada` ∈ [1, 5] quando preenchidos
- `cobertura_pct` ∈ [0, 100] quando preenchido
- **Aviso 5W2H** (não bloqueia): se faltam campos do 5W2H, o controle é
  marcado como descrição incompleta no log de validação

## Como entra no score X

O controle contribui para o ambiente do par (processo, risco) que mitiga,
através do **déficit de eficácia**:

```
deficit = 5 - eficacia_efetiva
```

Onde `eficacia_efetiva` combina autoavaliação e validação conforme o
`status_validacao` (peso decrescente da autoavaliação conforme a evidência
empírica aumenta — ver `docs/metodologia.md`):

| status_validacao | peso autoaval. | peso validação |
|------------------|----------------|----------------|
| apenas_autoavaliado | 1.0 | 0.0 |
| validado_documentalmente | 0.7 | 0.3 |
| validado_amostral | 0.4 | 0.6 |
| validado_completo | 0.1 | 0.9 |

Controle com eficácia validada alta **reduz** o score X (melhora o
ambiente). Controle sem validação contribui apenas com a autoavaliação,
que tem confiança menor.

## Relacionamentos

- `risco_id` → **B6**
- `processo_id` → **B1**
- `responsavel` → **B12** (opcional)
- Referenciado por **B2** (apontamentos sobre controles)

## Exemplo

```csv
id;acao;tipo;risco_id;processo_id;responsavel;local;frequencia;mecanismo;como;cobertura_pct;natureza;eficacia_autoavaliada;eficacia_validada;status_validacao
CTRL-CRED-002;Comite aprova operacoes acima de R$5M;credito;R0.U.7;P2.B.2.1;Comite de Credito;Sistema X + ata;semanal;manual;Voto qualificado 4/5;100;preventivo;4;3;validado_amostral
CTRL-CYBER-003;Monitoramento de acessos privilegiados;operacional;R0.U.5;P2.U.8.1;Ciberseguranca;SIEM;continuo;automatico;Alertas em tempo real;85;detectivo;4;;apenas_autoavaliado
```

## Nota metodológica

A separação entre `eficacia_autoavaliada` (o que a área diz) e
`eficacia_validada` (o que a 2ª linha confirma) é deliberada. Ela
materializa a **cobertura de transição**: a fração de controles que já
passou por validação independente. Um ambiente onde tudo é só
autoavaliado tem confiança epistêmica menor que um onde a 2ª linha já
testou — e o BooX reflete isso no peso, não escondendo a diferença.
