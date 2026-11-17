# Banco Modelo S.A. — instancia de exemplo

Banco multiplo **S2 ficticio**. Todos os dados sao sinteticos (ver
`../../LICENSE-DATA`). Esta instancia demonstra o BooX ponta a ponta:
vocabulario **local** (com marcas ficticias) traduzido para o **canonico**
via B_MAP, gerando o 20-box.

## Como rodar

Da raiz do repositorio:

```bash
python -m boox examples/banco_modelo_sa --out output
```

Abra `output/20box.html`. Saidas geradas:

- `20box.html` — mapa Impacto x Ambiente de Controles
- `detalhamento.csv` — uma linha por par processo x risco
- `parecer.md` — sumario executivo + pares criticos

### Por uma Visao especifica

```bash
python -m boox examples/banco_modelo_sa --out output --visao VIS_CONSIGNADO
python -m boox examples/banco_modelo_sa --out output --visao VIS_CYBER_LGPD
python -m boox examples/banco_modelo_sa --out output --visao VIS_CREDITO
python -m boox examples/banco_modelo_sa --out output --visao VIS_CONDUTA
```

## Os Books preenchidos (9 do Lite)

| Arquivo | Linhas | Conteudo |
|---------|--------|----------|
| B1_processos.csv | 28 | processos P0->P2 do banco |
| B6_riscos.csv | 17 | riscos locais (vocabulario do banco) |
| B6_vinculo_processo_risco.csv | 34 | pares avaliaveis (as bolhas) |
| B5_controles.csv | 20 | controles em 5W2H |
| B2_apontamentos.csv | 23 | apontamentos de varias fontes |
| B10_indicadores.csv | 16 | KRIs |
| B10_indicador_serie.csv | 96 | serie temporal dos KRIs (6 meses) |
| B8_externos.csv | 14 | sinais externos (BACEN, CVM, etc.) |
| B4_regulacao.csv | 9 | normas externas (CMN 4.557, 4.968, 4.893, BCB 265, Circ. 3.978, Lei 9.613, LGPD, CVM 30, ANBIMA) |
| B_TESTES_execucao.csv | 28 | execucoes de testes do canonico 1.5.0, com resultados variados |
| B_EVIDENCIA.csv | 21 | evidencias referenciadas pelas execucoes |
| B9_disciplinas.csv | 15 | disciplinas usadas |
| B7_visoes.csv | 5 | visoes registradas |
| B_MAP_taxonomia.csv | 37 | de-para local -> canonico |

## O de-para em acao

Os riscos e areas usam nomes **locais** (ex: risco `RL-07` "Risco de
Invasao Digital", area "Segmento Diamante", sigla "DICOI"). O
`B_MAP_taxonomia.csv` traduz cada um para o ID canonico
(`RL-07 -> R0.U.7`, `Segmento Diamante -> ORG.NEG.ALT`,
`DICOI -> ORG.CIN.CTI`). A engine resolve essa traducao antes de calcular.

## Regenerar

Os dados sao produzidos por um gerador deterministico:

```bash
cd examples/banco_modelo_sa
python _gerar.py
```

## Analise de suficiencia

Ao rodar `python -m boox`, alem do 20-box e do parecer, e gerado
`suficiencia.md` — um diagnostico que diz, por Book, se os campos
obrigatorios estao 100% preenchidos, quanto dos recomendados foi informado,
e lista alertas estruturais (hierarquia quebrada, riscos sem de-para,
controles com 5W2H incompleto, KRIs com serie curta). E o "raio-x" da
qualidade dos dados antes de confiar no mapa.

## Templates Excel

Os templates em `../../templates/*.xlsx` sao o ponto de partida para um
banco real preencher seus proprios dados. Cada template tem os campos
coloridos por categoria (obrigatorio/recomendado/opcional), listas
suspensas e uma aba de instrucoes.

## Leitura do relatorio de gap

Esta instancia executa **28 dos 380 testes** aplicaveis a um banco multiplo. O
relatorio de gap mostra, portanto, cobertura baixa de proposito: ele demonstra
a diferenca entre requisito **catalogado** e requisito **testado**. Todos os
testes do catalogo estao com status `proposto` (a validar contra o texto
oficial), e o BooX mede cobertura, nao prova conformidade.
