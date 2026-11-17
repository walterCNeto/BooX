# Templates dos Books

Planilhas Excel vazias, formatadas, para o banco preencher com seus dados e
exportar para CSV (separador `;`, UTF-8). Cada arquivo tem:

- cabeçalhos exatos conforme [`../schema/`](../schema/) (campos coloridos: vermelho = obrigatório, âmbar = recomendado, cinza = opcional);
- listas suspensas para os campos enumerados;
- aba **Instrucoes** com a descrição de cada campo.

## Quais preencher

| Template | Para que serve |
|---|---|
| B1_processos, B6_riscos, B6_vinculo_processo_risco | processos, riscos locais e pares avaliáveis (as bolhas do 20-box) |
| B5_controles, B2_apontamentos, B10_indicadores, B10_indicador_serie, B8_externos | controles, apontamentos, KRIs e sinais externos |
| B9_disciplinas, B7_visoes, B7_visao_filtros | disciplinas e visões |
| B4_regulacao, B4_vinculo_norma | normas que a casa adota e a quais riscos se vinculam |
| **B_TESTES_execucao** | **o que a casa executa**: um registro por teste do catálogo canônico executado, com resultado, data, evidência e apontamento |
| B_EVIDENCIA | catálogo das evidências citadas em B_TESTES_execucao |

O catálogo canônico de testes (`canonico/B_TESTES_canonico.csv`) não é
preenchido pelo banco: ele é mantido pelo projeto.

## Preenchimento de B_TESTES_execucao

- `teste_canonico_id`: id do catálogo (ex.: `TST.CMN4968.001`). Use apenas ids que existam no canônico da sua versão.
- `resultado_ultimo`: `conforme`, `parcialmente_conforme`, `nao_conforme`, `nao_executado` ou `na`. Recomenda-se justificar o `na` em `observacoes`.
- `evidencia_id`: id de B_EVIDENCIA; recomenda-se evidência para todo resultado diferente de `nao_executado` e `na`.
- `apontamento_id`: recomendado para `nao_conforme` (problema concreto vira apontamento).
- `frequencia_real`: com que frequência a casa executa de fato; compare com a `frequencia_minima` do catálogo.
- Um teste não executado fica de fora do arquivo e aparece no gap como "sem execução". O BooX mede cobertura, não prova conformidade.

## Regenerar

```bash
python templates/_gerar_templates.py
```
