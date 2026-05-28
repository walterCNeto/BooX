# Metodologia BooX — Score e 20-box

Este documento define como o BooX calcula a posição de cada par
**processo × risco** no 20-box: o score de Impacto (eixo Y) e o score de
Ambiente de Controles (eixo X), e como ambos se traduzem em níveis e em
Prioridade de Tratamento.

## 1. A unidade de avaliação

O BooX avalia cada **par (processo, risco)** de forma independente. A fonte
desses pares é o arquivo `B6_vinculo_processo_risco.csv`. Cada linha é uma
avaliação. O mesmo risco em três processos gera três avaliações, porque o
ambiente de controles pode diferir entre eles.

## 2. Eixo Y — Impacto

O score Y mede o **impacto inerente** do risco naquele processo, em escala
0 a 5.

### 2.1 Origem

Prioridade de fontes (a primeira disponível prevalece):

1. `materialidade_inerente` declarada no vínculo (B6) — **prioritária**
2. Criticidade BIA do processo (B1 `criticidade_bia`) — fallback
3. Default = 3 (Médio) se nada disponível

### 2.2 Conversão para nível

| materialidade | score_Y | Nível de Impacto |
|---------------|---------|------------------|
| 1 | 0.5 | Imaterial |
| 2 | 1.5 | Baixo |
| 3 | 2.5 | Médio |
| 4 | 3.5 | Alto |
| 5 | 4.5 | Elevado |

### 2.3 Faixas do eixo Y

| score_Y | Nível |
|---------|-------|
| [0.0, 1.0) | Imaterial |
| [1.0, 2.0) | Baixo |
| [2.0, 3.0) | Médio |
| [3.0, 4.0) | Alto |
| [4.0, 5.0] | Elevado |

## 3. Eixo X — Ambiente de Controles

O score X mede a **insuficiência** do ambiente de controles, em escala
0 a 100. **Score alto = ambiente pior** (mais sinais negativos). Score
baixo = ambiente adequado.

### 3.1 Fórmula

```
score_X = clip(
      f_apontamentos
    + f_controles
    + f_indicadores
    + f_externos
    + f_cobertura
  , 0, 100)
```

Cada componente é descrito abaixo. Os pesos são **parâmetros ajustáveis**
(arquivo de configuração `boox/config.py`); os valores aqui são os
defaults calibrados para um banco múltiplo S2.

### 3.2 f_apontamentos (de B2)

Apontamentos abertos, em tratamento ou vencidos vinculados ao par:

```
base_severidade = {critico: 4.0, alto: 2.0, medio: 1.0, baixo: 0.5}
por apontamento:
    contrib = base_severidade[severidade]
    se origem == regulador: contrib *= 2.0
    se status == vencido:   contrib += 1.5
f_apontamentos = min(soma(contrib) * 4.0, 40)   # escala para 0-100, cap 40
```

### 3.3 f_controles (de B5)

Déficit de eficácia dos controles que mitigam o par:

```
para cada controle do par:
    eficacia_efetiva = peso_auto * eficacia_autoavaliada
                     + peso_val  * eficacia_validada
    (pesos conforme status_validacao — ver abaixo)
    deficit = 5 - eficacia_efetiva
eficacia_media_deficit = media(deficit) dos controles do par
f_controles = eficacia_media_deficit * 5.0   # escala 0-25 aprox.

se o par NÃO tem nenhum controle declarado:
    f_controles = 15  # penalidade por ausência de controle conhecido
```

Pesos por status de validação:

| status_validacao | peso_auto | peso_val |
|------------------|-----------|----------|
| apenas_autoavaliado | 1.0 | 0.0 |
| validado_documentalmente | 0.7 | 0.3 |
| validado_amostral | 0.4 | 0.6 |
| validado_completo | 0.1 | 0.9 |

Quando `eficacia_validada` está vazia, usa-se apenas a autoavaliada
independentemente do status.

### 3.4 f_indicadores (de B10)

KRIs que monitoram o par, no período mais recente:

```
por KRI:
    se status == vermelho: contrib = 3.0
    se status == amarelo:  contrib = 1.0
    se status == verde:    contrib = 0.0
    se tendencia == piora (6m): contrib += 1.0
f_indicadores = min(soma(contrib) * 2.0, 20)   # cap 20
```

### 3.5 f_externos (de B8)

Sinais externos vinculados ao par (diretamente, pelo risco, ou pela
disciplina do risco):

```
contribuições com caps por fonte:
    bacen procedente:    0.5 cada, cap 6.0
    bacen tendencia alta: +1.5
    cvm julgado:         2.0 cada, cap 6.0
    cvm em curso:        1.0 cada, cap 6.0
    anbima carta:        0.3 cada, cap 3.0
    anbima termo:        0.5 cada, cap 3.0
    anbima julgamento:   1.5 cada, cap 3.0
    procon procedente:   0.3 cada, cap 3.0
    midia sev>=4:        1.0 cada, cap 4.0
    midia sev==3:        0.4 cada, cap 4.0
    reclame_aqui queda>=0.5: ate 2.0
f_externos = min(soma das contribuições, 25)   # cap global 25
```

### 3.6 f_cobertura (penalidade por desconhecimento)

A **cobertura** mede se o par recebeu algum sinal nos últimos 12 meses
(apontamento, controle avaliado, KRI ativo, sinal externo). Cobertura baixa
significa "ambiente desconhecido" — e o default ignorante deve ser
pessimista:

```
o par "tem sinal" se: tem apontamento OU controle com eficacia OU KRI ativo OU sinal externo

cobertura é calculada por agrupamento (processo, ou disciplina):
    cobertura = pares_com_sinal / pares_declarados

penalidade aplicada ao par sem sinal próprio, conforme cobertura do grupo:
    cobertura >= 70%:  f_cobertura = 0
    40% <= cob < 70%:  f_cobertura = 5
    cobertura < 40%:   f_cobertura = 10
```

Um par totalmente sem sinais, em um grupo de baixa cobertura, recebe
penalidade — porque "não sabemos" não deve ser lido como "está tudo bem".

### 3.7 Conversão para nível do eixo X

| score_X | Símbolo | Nível |
|---------|---------|-------|
| [0, 20) | `++` | Adequado |
| [20, 40) | `+` | Bom |
| [40, 60) | `0` | Neutro |
| [60, 80) | `-` | Atenção |
| [80, 100] | `--` | Crítico |

## 4. A célula — Prioridade de Tratamento

Combinando o nível de Impacto (Y) e o nível de Ambiente (X), cada par cai
em uma das 25 células, classificada em cinco níveis de Prioridade:

```
                          Ambiente de Controles
              --        -         0         +        ++
Elevado    CRÍTICO   CRÍTICO   ALTO      MÉDIO     MÉDIO
Alto       CRÍTICO   ALTO      MÉDIO     MÉDIO     BAIXO
Médio      ALTO      MÉDIO     MÉDIO     BAIXO     BAIXO
Baixo      MÉDIO     MÉDIO     BAIXO     BAIXO     OK
Imaterial  BAIXO     BAIXO     OK        OK        OK
```

A matriz é definida explicitamente (não por fórmula), permitindo ajuste
fino pela casa conforme seu apetite a risco.

## 5. Agregação para níveis superiores

Quando se quer o ambiente de um R0 (agregando seus R1, R2...) ou de um
processo (agregando seus subprocessos), o BooX faz **média ponderada pela
materialidade**:

```
score_agregado = soma(score_par * materialidade_par) / soma(materialidade_par)
```

Isso garante que pares mais materiais dominam a leitura agregada — um
problema crítico em um sub-risco material não é diluído por muitos
sub-riscos imateriais bem controlados.

## 6. Por que Impacto × Ambiente, e não Impacto × Probabilidade

O 20-box do BooX usa **Ambiente de Controles** no eixo X, não
probabilidade. Esta é uma escolha metodológica deliberada.

A matriz Impacto × Probabilidade nasce em frameworks de avaliação de
projetos *a priori* (PMI, ISO 31000 clássica), onde se estima a chance de
um evento futuro sem histórico. Para **processos em operação**, com dados
acumulados — apontamentos, KRIs, perdas, sinais externos — "probabilidade"
vira ou frequência observada (que é métrica, não estimativa) ou opinião
que ignora a evidência disponível.

O regime regulatório brasileiro (Res. CMN 4.557, Res. BCB 265, princípios
BCBS de risco operacional) constrói um sistema de **monitoramento empírico
contínuo** baseado em frequência e severidade observadas, indicadores e
efetividade testada de controles. Nesse regime, comprimir a riqueza desses
sinais em "probabilidade qualitativa" descarta informação.

O eixo "Ambiente de Controles" preserva essa riqueza: ele é uma agregação
multidimensional e auditável de tudo que se sabe sobre como o risco está
sendo efetivamente endereçado. A matriz Impacto × Probabilidade permanece
útil para **riscos emergentes sem histórico** e **riscos de cauda** — que
podem ser tratados em registro complementar — mas não como base de
avaliação de processos vivos.

## 7. Parâmetros ajustáveis

Todos os pesos, caps e cortes descritos aqui vivem em `boox/config.py` e
podem ser sobrescritos por um arquivo de configuração da casa. A
recalibração é legítima e esperada — cada instituição tem apetite a risco
próprio. O que o BooX garante é que a metodologia seja **explícita,
auditável e reproduzível**: dado o mesmo input e a mesma configuração, o
resultado é sempre o mesmo.
