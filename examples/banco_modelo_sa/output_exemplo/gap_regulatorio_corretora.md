# Analise de Gap Regulatorio — BooX

Tipo de instituicao: **corretora**
Testes canonicos aplicaveis: **6**

## Cobertura por regulador

| Regulador | Total | Atendido | Parcial | Nao conforme | Sem execucao | N/A |
|-----------|-------|----------|---------|--------------|--------------|-----|
| **BACEN** | 3 | 1 (33.3%) | 0 | 1 | 1 | 0 |
| **COAF** | 3 | 0 (0.0%) | 1 | 1 | 1 | 0 |

## Gaps criticos (alta criticidade sem atendimento): **3**

- **[BACEN]** TST.SEED.CYBER.001 — MFA em acesso privilegiado a sistemas criticos (estado: nao_conforme)
- **[COAF]** TST.SEED.PLDFT.001 — Identificacao e classificacao de PEP no cadastro (estado: parcial)
- **[COAF]** TST.SEED.PLDFT.002 — SLA de tratamento de alertas de alta prioridade (estado: nao_conforme)

## Controles orfaos (sem teste canonico associado): **15**

Podem ser controles especificos do banco (legitimos) ou trabalho sem sustentacao regulatoria. Vale revisar.

- CT-001 — Comite de credito aprova operacoes acima de limite
- CT-002 — Motor de decisao automatizado com score
- CT-003 — Validacao independente anual do modelo
- CT-004 — Limites de VaR e stop loss na mesa
- CT-005 — Monitoramento de gaps de liquidez
- CT-008 — SOC 24x7 e resposta a incidentes
- CT-010 — Plano de continuidade e DR testado
- CT-011 — Dupla checagem na liquidacao
- CT-012 — Selo de suitability na venda
- CT-013 — Antifraude em canais digitais
- CT-014 — Mapa de privacidade e base legal
- CT-017 — Limite cambial e hedge
- CT-018 — Politica de cobranca e renegociacao
- CT-019 — Due diligence de fornecedores criticos
- CT-020 — Conciliacao diaria de retaguarda

## Fatores de Risco descobertos: **5**

FRs canonicos cujos testes NAO estao atendidos — sinal de vulnerabilidade.

- FR.CYBER.001 (testes: 1 · atendidos: 0)
- FR.CYBER.002 (testes: 1 · atendidos: 0)
- FR.PLDFT.001 (testes: 1 · atendidos: 0)
- FR.PLDFT.002 (testes: 1 · atendidos: 0)
- FR.PLDFT.003 (testes: 1 · atendidos: 0)

---
_Gerado pela engine de gap regulatorio do BooX._