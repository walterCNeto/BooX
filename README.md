# BooX — Framework de Risco Operacional baseado em Books

**BooX** é um framework aberto para gestão de risco operacional em
instituições financeiras brasileiras. Organiza todo o ecossistema de
controles internos em **Books** interligados e gera, a partir deles, um
**20-box** dinâmico de Impacto × Ambiente de Controles para qualquer
recorte que o CRO precise: produto, processo, disciplina, segmentação ou
visão ponta-a-ponta.

> O nome vem dos **X Books** necessários para que o framework funcione de
> forma integrada. Cada Book é uma fonte de dados que conversa com as
> demais por chaves comuns. Quando algo muda em qualquer Book, o framework
> inteiro pode ser regenerado.

## A ideia em uma frase

Você preenche os Books com os dados da sua casa, roda a ferramenta, e ela
plota onde cada risco está no mapa **Impacto × Ambiente de Controles** —
combinando autoavaliação, apontamentos, indicadores e sinais externos
(BACEN, CVM, ANBIMA, Procon, mídia) em um score auditável.

## O 20-box

O coração do BooX é um mapa **5 × 5**:

```
                          Ambiente de Controles
              --        -         0         +        ++
           Crítico   Atenção   Neutro     Bom    Adequado
          ┌────────┬────────┬────────┬────────┬────────┐
Elevado   │CRÍTICO │CRÍTICO │ALTO    │MÉDIO   │MÉDIO   │
          ├────────┼────────┼────────┼────────┼────────┤
Alto      │CRÍTICO │ALTO    │MÉDIO   │MÉDIO   │BAIXO   │
          ├────────┼────────┼────────┼────────┼────────┤
Médio     │ALTO    │MÉDIO   │MÉDIO   │BAIXO   │BAIXO   │
          ├────────┼────────┼────────┼────────┼────────┤
Baixo     │MÉDIO   │MÉDIO   │BAIXO   │BAIXO   │  OK    │
          ├────────┼────────┼────────┼────────┼────────┤
Imaterial │BAIXO   │BAIXO   │  OK    │  OK    │  OK    │
          └────────┴────────┴────────┴────────┴────────┘
```

- **Eixo Y — Impacto** (inerente do risco): Imaterial · Baixo · Médio · Alto · Elevado
- **Eixo X — Ambiente de Controles**: Crítico (`--`) · Atenção (`-`) · Neutro (`0`) · Bom (`+`) · Adequado (`++`)
- **Célula — Prioridade de Tratamento**: Crítico · Alto · Médio · Baixo · OK

O eixo X é **monotonicamente crescente**: quanto mais à direita, melhor o
ambiente de controles em relação ao perfil do risco. `++` significa
ambiente **adequado** ao risco — não "excesso de controle".

## Os Books

| Book | Nome | Conteúdo |
|------|------|----------|
| **B1** | Processos | Processos do banco, em qualquer nível (P0→P4) |
| **B2** | Apontamentos | Apontamentos de qualquer fonte (CI, auditoria, compliance, regulador) |
| **B3** | Normas e Procedimentos Internos | Normas, documentações e procedimentos internos |
| **B4** | Regulação e Circulares | Regulação externa: leis, CMN, BCB, CVM, SUSEP, ANBIMA |
| **B5** | Controles | Controles em formato 5W2H, por tipo (ICAAP, operacional, crédito, etc.) |
| **B6** | Riscos | Riscos com taxonomia hierárquica (R0→R4) |
| **B7** | Visões | Recortes que o banco quer ter: produto, processo, E2E, segmento |
| **B8** | Reguladores e Ouvidoria | Procedentes BACEN, Procon, Ouvidoria, sinais externos |
| **B9** | Disciplinas | Crédito, Mercado, Liquidez, Operacional, Cyber, LD, Fraude, etc. |
| **B10** | Indicadores | KRIs de risco operacional (metas de redução de falhas/perdas) |
| **B11** | Siglas | Glossário de siglas internas |
| **B12** | Pessoas | Pessoas e atividades (owners, responsáveis) |
| **B13** | Segmentações de Negócio | Varejo, Atacado, Private, Financeira, etc. |

### BooX Lite (esta versão)

Esta versão inicial (**v0.1, Lite**) usa o subconjunto de **9 Books**
necessário para gerar o 20-box:

**B1, B2, B4, B5, B6, B7, B8, B9, B10**

Os Books B3, B11, B12 e B13 são opcionais nesta versão e entram em
releases futuros. O framework foi desenhado para que adicioná-los depois
não quebre nada — eles enriquecem, não alteram, o cálculo.

## Como funciona

```
   Books preenchidos (CSV / Excel)
            │
            ▼
   ┌─────────────────┐
   │  boox load      │  lê e valida os books
   ├─────────────────┤
   │  boox compute   │  calcula score X (ambiente) e Y (impacto)
   ├─────────────────┤
   │  boox view      │  aplica filtros de uma Visão (B7)
   ├─────────────────┤
   │  boox render    │  gera 20-box, parecer e detalhamento
   └─────────────────┘
            │
            ▼
   output/
   ├── 20box.html         mapa interativo
   ├── detalhamento.csv   uma linha por par processo × risco
   ├── parecer.md         sumário executivo + riscos críticos
   └── log_validacao.md   inconsistências encontradas na entrada
```

## Quickstart

```bash
# instalar
pip install -e .

# rodar com o Banco Modelo S.A. (dados de exemplo)
boox run examples/banco_modelo_sa/ --output output/

# abrir output/20box.html no navegador
```

## Estrutura do repositório

```
BooX/
├── boox/                    Código da ferramenta (Python)
├── schema/                  Especificação compacta dos Books
│   └── books/               Uma página por Book
├── templates/               Templates Excel para preencher
├── examples/
│   └── banco_modelo_sa/     Banco Modelo S.A. (9 books preenchidos)
└── docs/                    Metodologia e documentação
```

## Modelo conceitual

O BooX trabalha com a unidade **par processo × risco**: cada risco, em
cada processo onde ele aparece, é uma linha de avaliação independente. O
mesmo risco pode ter ambiente de controles diferente em processos
diferentes.

Para cada par, o BooX combina:

- **Impacto (eixo Y)**: materialidade inerente do risco, calibrada pela casa
- **Ambiente de controles (eixo X)**: agregação multidimensional de
  apontamentos, eficácia de controles, indicadores (KRIs), sinais externos
  e cobertura de avaliação

Ver `docs/metodologia.md` para a formulação completa do score.

## Licença

- **Código**: MIT — ver [`LICENSE`](LICENSE)
- **Dados e catálogos** (incluindo Banco Modelo S.A.): CC BY 4.0 — ver [`LICENSE-DATA`](LICENSE-DATA)

## Status

**v0.1 (Lite)** — em desenvolvimento. Subconjunto de 9 Books, CLI Python,
20-box HTML estático. Sem frontend web nem banco de dados — roda local a
partir de arquivos.

## Autor

Walter C. Neto — [github.com/walterCNeto](https://github.com/walterCNeto)
