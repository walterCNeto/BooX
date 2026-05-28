# Banco Modelo S.A. — Conjunto de dados de exemplo

O **Banco Modelo S.A.** é uma instituição financeira **fictícia** usada
para demonstrar o BooX. Todos os dados são sintéticos.

## Perfil

- **Tipo**: Banco múltiplo
- **Segmento prudencial**: S2
- **Atuação**: comercial (crédito PF/PJ), câmbio, asset management,
  distribuição, gestão fiduciária
- **Núcleos de processo**: Universal (U), Bancário (B), Mercado de
  Capitais (MC), Conglomerado (CG)

## Status

**Em construção (Fase 2).** Esta pasta conterá os 9 Books do BooX Lite
preenchidos com dados realistas e internamente consistentes:

```
banco_modelo_sa/
├── B1_processos.csv
├── B2_apontamentos.csv
├── B4_regulacao.csv
├── B4_vinculo_norma.csv
├── B5_controles.csv
├── B6_riscos.csv
├── B6_vinculo_processo_risco.csv
├── B7_visoes.csv
├── B7_visao_filtros.csv
├── B8_externos.csv
├── B9_disciplinas.csv
├── B10_indicadores.csv
└── B10_indicador_serie.csv
```

## Visões planejadas

O Banco Modelo S.A. terá Visões registradas demonstrando recortes típicos:

- **Consignado INSS** (visão produto)
- **Crédito End-to-End** (visão E2E)
- **Cyber e LGPD** (visão disciplina)
- **Conduta e Suitability** (visão disciplina)
- **Câmbio Comercial** (visão processo)

## Aviso

Instituição, dados, pessoas e eventos são fictícios e sintéticos, criados
para demonstração e ensino. Ver `../../LICENSE-DATA`.
