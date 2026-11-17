# Analise de Gap Regulatorio — BooX

Tipo de instituicao: **corretora**
Testes canonicos aplicaveis: **260** (data de referencia: 2026-11-17)
Atividades consideradas: padrao (todas)
Tipos de fundo considerados: padrao (todos)

> O BooX mede cobertura, nao prova conformidade.

## Status do teste: ativo (validado) x proposto

Percentual validado (ativos / aplicaveis): **73.5%**

| Status | Total | Atendido | Parcial | Nao conforme | Sem execucao | N/A |
|--------|-------|----------|---------|--------------|--------------|-----|
| **ativo** | 191 | 6 (3.1%) | 3 | 3 | 179 | 0 |
| **proposto** | 69 | 0 (0.0%) | 0 | 0 | 69 | 0 |

Testes `proposto` sao sementes ainda nao validados: atende-los nao prova conformidade.

Testes equivalentes (`equivale_a`) contados uma vez: 3 deduplicado(s) em 3 grupo(s).

## Cobertura por regulador

| Regulador | Total | Atendido | Parcial | Nao conforme | Sem execucao | N/A |
|-----------|-------|----------|---------|--------------|--------------|-----|
| **ANBIMA** | 19 | 1 (5.3%) | 1 | 1 | 16 | 0 |
| **BACEN** | 74 | 4 (5.4%) | 1 | 1 | 68 | 0 |
| **BSM** | 14 | 0 (0.0%) | 0 | 0 | 14 | 0 |
| **COAF** | 3 | 0 (0.0%) | 0 | 0 | 3 | 0 |
| **CVM** | 150 | 1 (0.7%) | 1 | 1 | 147 | 0 |

## Requisitos regulatorios nao atendidos — **254**

Testes canonicos aplicaveis que NAO estao em estado 'atendido'. Inclui parcial, nao conforme e sem execucao.

### Criticidade alta — 160
- **[ANBIMA]** TST.ANBSUIT.001 — Documento escrito de regras e procedimentos de suitability (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.002 — Coleta de informacoes de objetivo, situacao financeira e conhecimento (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.003 — Atualizacao do perfil no prazo da regulacao (estado: parcial)
- **[ANBIMA]** TST.ANBSUIT.006 — Vedacao de recomendar produto inadequado ou sem perfil valido (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.007 — Alerta e declaracao expressa do investidor (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.009 — Classificacao dos produtos e sua atualizacao (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.013 — Regras para produtos complexos (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.014 — Classificacao automatica como complexo (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.017 — Indicadores quantitativos do laudo (estado: nao_conforme)
- **[BSM]** TST.BSM.PQO.CAD.001 — RPA/NPA com procedimentos obrigatorios (19 pontos) (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.004 — Cadastro com criterios e periodicidade de atualizacao (intervalo maximo 5 anos) (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.006 — Conteudo minimo do cadastro do Cliente (7 pontos obrigatorios) (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.007 — Firmar contrato de intermediacao com conteudo minimo B3 (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.008 — Contrato de custodia com disposicoes regulamentares (Agentes de Custodia) (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.011 — Cadastro simplificado de Cliente investidor nao residente (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.012 — Cadastro do Cliente nos sistemas internos identico ao da B3 (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.002 — Diretrizes minimas da politica (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.003 — Diretrizes para procedimentos (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.008 — Politica documentada, aprovada e atualizada (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.009 — Estrutura de governanca de PLD-FT (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.010 — Diretor responsavel indicado ao BCB (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.011 — Avaliacao interna de risco: perfis considerados (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.012 — Avaliacao interna: probabilidade, impacto e categorias (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.014 — Avaliacao interna aprovada e levada a ciencia (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.015 — Revisao bienal da avaliacao interna (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.016 — Procedimentos para conhecer clientes (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.017 — Manual de conheca seu cliente (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.018 — Informacoes cadastrais em sistemas informatizados (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.019 — Verificacao e validacao da identidade (estado: parcial)
- **[BACEN]** TST.CIRC3978.020 — Dados minimos de identificacao (estado: sem_execucao)

### Criticidade media — 86
- **[ANBIMA]** TST.ANBSUIT.004 — Perfil identificado e tratamento de recusa (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.005 — Excecao e suitability simplificado para produtos automaticos (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.008 — Classificacao do investidor em no minimo tres perfis (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.010 — Metodologia de classificacao de risco dos produtos (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.016 — Controles testados e alteracoes de metodologia no laudo (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.018 — Plano de acao para divergencias (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.019 — Documentos passiveis de verificacao (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.002 — Disponibilizacao da RPA/NPA aos Clientes antes das operacoes (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.003 — Comunicacao imediata de alteracoes da RPA/NPA e guarda por 5 anos (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.005 — Sistemas alternativos de cadastro (inclusive eletronico) verificaveis (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.009 — Contrato com criterios de cobranca de corretagem/custodia/custos (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.010 — RPA/NPA como parte integrante do contrato de intermediacao (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.013 — Lista de pessoas autorizadas a emitir Ordens atualizada perante a B3 (estado: sem_execucao)
- **[BSM]** TST.BSM.PQO.CAD.014 — Controle para identificacao de clientes qualificados e profissionais (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.004 — Comprometimento da alta administracao (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.005 — Formalizacao das opcoes de centralizacao (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.006 — Politica aplicada a unidades no exterior (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.007 — Divulgacao da politica (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.027 — Administradores e representantes de clientes (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.032 — PEP no exterior e prazo de cinco anos (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.034 — Registro: nao residentes e cambio (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.035 — Registro de operacoes dentro da mesma instituicao (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.037 — Contrato com terceiros de arranjo de pagamento (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.042 — Provisionamento de saques a partir de R$ 50.000 (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.043 — Registro de boletos pagos em especie (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.051 — Analise no Pais e sem terceirizacao (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.052 — Nuvem e processamento no monitoramento (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.059 — Indicacao de PEP e terrorismo nas comunicacoes (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.060 — Declaracao de nao ocorrencia (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.061 — Habilitacao no Siscoaf (estado: sem_execucao)

### Criticidade baixa — 8
- **[ANBIMA]** TST.ANBSUIT.011 — Fundamentacao de metodologia diversa da referencia (estado: sem_execucao)
- **[ANBIMA]** TST.ANBSUIT.012 — Categorias minimas de produtos (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.013 — Uso de avaliacoes de entidades publicas (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.038 — Informacao de CPF e CNPJ na compensacao de cheques (estado: sem_execucao)
- **[BACEN]** TST.CIRC3978.058 — Justificativa para alteracao ou cancelamento tardio (estado: sem_execucao)
- **[CVM]** TST.CVM035.032 — Divulgacao e disponibilidade das regras internas (estado: sem_execucao)
- **[CVM]** TST.CVM035.033 — Orientacao sobre mecanismo de ressarcimento (estado: sem_execucao)
- **[CVM]** TST.CVM035.040 — Orientacoes de seguranca ao cliente (estado: sem_execucao)

## Controles internos (nao regulatorios) — **10**

Controles do banco (B5) sem teste canonico especifico mapeado. Analise por moldura:
- **10** atendem norma-moldura (ex: CMN 4.557 para risco operacional) — legitimos, mas sem teste pontual mapeado
- **0** sem moldura inferida — candidatos a revisao

### Agregado por moldura inferida

| Moldura | Qtd controles |
|---------|---------------|
| **CMN 4.557** | 9 |
| **LGPD (Lei 13.709)** | 1 |

### Controles que atendem moldura (amostra)
- CT-001 (CMN 4.557) — Comite de credito aprova operacoes acima de limite
- CT-002 (CMN 4.557) — Motor de decisao automatizado com score
- CT-003 (CMN 4.557) — Validacao independente anual do modelo
- CT-004 (CMN 4.557) — Limites de VaR e stop loss na mesa
- CT-005 (CMN 4.557) — Monitoramento de gaps de liquidez
- CT-011 (CMN 4.557) — Dupla checagem na liquidacao
- CT-013 (CMN 4.557) — Antifraude em canais digitais
- CT-014 (LGPD (Lei 13.709)) — Mapa de privacidade e base legal
- CT-017 (CMN 4.557) — Limite cambial e hedge
- CT-018 (CMN 4.557) — Politica de cobranca e renegociacao

## Fatores de Risco descobertos: **6**

FRs canonicos cujos testes NAO estao atendidos — sinal de vulnerabilidade.

- FR.CYBER.001 (testes: 1 · atendidos: 0)
- FR.CYBER.002 (testes: 1 · atendidos: 0)
- FR.CYBER.003 (testes: 1 · atendidos: 0)
- FR.PLDFT.001 (testes: 1 · atendidos: 0)
- FR.PLDFT.002 (testes: 1 · atendidos: 0)
- FR.PLDFT.003 (testes: 1 · atendidos: 0)

## Fora de vigencia — **0**

Testes nao contados: vigencia_fim anterior a 2026-11-17 ou vigencia_inicio futura.

_Nenhum._

## Normas excluidas para o tipo de instituicao — **6**

Normas com testes cuja aplicabilidade nao inclui o tipo informado (nao contados).

- RES_CMN_4557 — 38 teste(s) (norma inteira)
- RES_CMN_4893 — 24 teste(s) (parcial)
- RES_CMN_4968 — 45 teste(s) (norma inteira)
- RES_CNSP_416 — 25 teste(s) (norma inteira)
- RES_CVM_175 — 82 teste(s) (norma inteira)
- RES_CVM_21 — 33 teste(s) (norma inteira)

## Nao aplicaveis pela atividade — **0**

Testes cuja coluna `atividades` nao intersecta as atividades consideradas (nao contados).

_Nenhum._

## Nao aplicaveis pelo tipo de fundo — **0**

Testes cuja coluna `tipos_fundo` nao intersecta os tipos de fundo considerados (nao contados).

_Nenhum._

---
_Gerado pela engine de gap regulatorio do BooX._