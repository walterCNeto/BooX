# A Cadeia Regulamentar do BooX (Fase 1)

Modelo hierarquico completo que conecta a regulacao ate o teste
operacionalizavel.

## A cadeia, em 6 niveis

```
   Processo (P0 → P1 → P2 → P3 → P4)   [B1]
             ↓
   Risco R4 (mais granular)             [B6, estendido R0→R4]
             ↓
   Fator de Risco (FR)                  [B_FR_canonico — NOVO]
             ↓
   Controle esperado                    [B_TESTES.controle_esperado]
             ↓
   Teste                                [B_TESTES_canonico — NOVO]
             ↓
   Evidencia                            [B_EVIDENCIA — NOVO]
```

## Niveis

1. **Processo** — onde o risco se materializa (B1).
2. **Risco R4** — "o que pode dar errado" no nivel mais fino. Antes do
   BooX so tinha R0; agora estende ate R4 (ex: "credencial admin sem MFA
   em sistema critico").
3. **Fator de Risco (FR)** — causa-raiz especifica. Um mesmo R4 pode ter
   varios FRs. Pede controle proprio.
4. **Controle esperado** — o que a norma EXIGE que exista. Nao e o
   controle real do banco (B5); e o controle-alvo. Gap = esperado sem
   real equivalente.
5. **Teste** — como verificar se o controle funciona. Operacionalizavel.
6. **Evidencia** — o que comprova o atendimento.

## Camadas

### Canonica (fixa, igual para todos)
- `B_TESTES_canonico.csv` — todos os testes dos reguladores. Colunas opcionais de aplicabilidade e vigencia: `aplicabilidade` (tipos de instituicao), `atividades` (lista com `|` do enum `atividade`; vazio = qualquer atividade), `tipos_fundo` (lista com `|` do enum `tipo_fundo`: fif, fidc, fii, fip; vazio = qualquer tipo), `equivale_a`, `vigencia_inicio`, `vigencia_fim`, `revogada_por`. Um teste se aplica quando o tipo confere E (`atividades` vazio OU intersecta as atividades declaradas); a mesma regra vale para `tipos_fundo`; sem declarar atividades nem tipos de fundo, vale o filtro so por tipo de instituicao.
- `B_FR_canonico.csv` — biblioteca de Fatores de Risco
- Riscos R4 em `B6_riscos_canonico.csv`

### Local (cada banco)
- `B_TESTES_execucao.csv` — quais testes o banco executa
- `B_EVIDENCIA.csv` — evidencias que o banco possui

## Aplicabilidade por tipo de instituicao

Cada teste declara `aplicabilidade = banco_multiplo | corretora | dtvm |
seguradora | cooperativa | ...`. Uma corretora ativa filtro "corretora" e
ve apenas seus ~340 testes; um banco multiplo ve os seus.

## Analise de Gap Regulatorio

`python -m boox.gap_regulatorio <pasta> --tipo <tipo>` responde:

1. **Cobertura por regulador** — % de testes aplicaveis atendidos
2. **Gaps criticos** — testes alta criticidade sem controle real
3. **Controles orfaos** — controles B5 sem teste canonico associado
4. **Fatores de Risco descobertos** — FR sem controle real

## Status dos testes-seed

Todos os testes atuais (`TST.SEED.*`) estao com status **`proposto`** —
sao arcabouco demonstrativo, NAO conteudo regulatorio validado. A Fase 2
trara o piloto BSM PQO com testes `ativos` rastreados a fonte oficial.
