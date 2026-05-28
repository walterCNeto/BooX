# B_MAP — Book de De-Para (Rosetta)

O **B_MAP** é a ponte entre o vocabulário **local** de um banco (com suas
marcas, siglas e nomes próprios) e o vocabulário **canônico** do BooX
(genérico, igual para todos). É o que permite cada banco entregar suas
tabelas como elas são e mesmo assim falar a língua comum do framework.

## O problema que resolve

Nenhum banco tem os dados no formato canônico do BooX. O banco tem:

- "Personnalité", "Prime", "Uniclass" — marcas de segmento
- "Risco de invasão de sistemas" — nome local de um risco
- "Comitê de Crédito Plus" — nome local de um controle
- "DICOI", "VICRI" — siglas internas de áreas

O B_MAP traduz cada termo local para o ID canônico correspondente:

```
"Personnalité"               → ORG.NEG.ALT (Alta Renda)
"Risco de invasao de sistemas" → R0.U.7 (Risco Cibernetico)
"Comite de Credito Plus"     → controle tipo credito
"DICOI"                      → ORG.CIN.CTI (Controles Internos)
```

## As duas camadas

```
CAMADA CANONICA (fixa, em canonico/)
  - B_ORG_dominios, B_ORG_areas        (organizacao)
  - B6_riscos_canonico                 (riscos R0)
  - B9_disciplinas_canonico            (disciplinas)
  - enums fixos (severidade, origem, frequencia...)
        ▲
        │  B_MAP traduz
        ▼
CAMADA LOCAL (especifica de cada banco)
  - tabelas do banco, no vocabulario do banco
```

A camada canônica **nunca muda** entre bancos. A camada local é livre. O
B_MAP é o dicionário que liga as duas, e é um **ativo permanente** de cada
banco — construído uma vez, reusado a cada ciclo.

## Arquivo

`B_MAP_taxonomia.csv`

## Colunas

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | string | sim | ID único do mapeamento |
| `dominio` | enum | sim | `organizacao`, `risco`, `disciplina`, `processo`, `controle`, `segmento` |
| `termo_local` | string | sim | Texto exato como o banco escreve |
| `termo_local_id` | string | não | ID interno do banco, se houver |
| `canonico_id` | string | sim | ID canônico BooX correspondente |
| `confianca_ia` | enum | não | `alta`, `media`, `baixa` (sugestão automática) |
| `metodo` | enum | não | `exato`, `similaridade`, `llm`, `manual` |
| `justificativa` | string | não | Por que esse mapeamento foi sugerido |
| `status` | enum | sim | `sugerido`, `aprovado`, `rejeitado`, `ajustado` |
| `aprovado_por` | string | não | Quem revisou e aprovou |
| `data_revisao` | data | não | Quando foi revisado |
| `notas` | string | não | Observações do revisor |

## Validações

- `id` único
- `dominio` ∈ {organizacao, risco, disciplina, processo, controle, segmento}
- `canonico_id` **deve existir** no Book canônico correspondente ao `dominio`
  (esta é a regra anti-alucinação — ver abaixo)
- `status` ∈ {sugerido, aprovado, rejeitado, ajustado}
- Apenas mapeamentos com `status = aprovado` ou `ajustado` são usados no cálculo

## A engine de de-para (anti-alucinação)

O B_MAP pode ser preenchido manualmente ou **proposto por IA**. Quando por
IA, a engine opera em três camadas, da mais segura para a mais arriscada:

### Camada 1 — Match exato (zero IA)
Se o `termo_local` já existe em um B_MAP de ciclo anterior (ou em uma
tabela de sinônimos conhecidos), reusa o mapeamento. Determinístico, sem
risco.

### Camada 2 — Match por similaridade (IA determinística)
Calcula similaridade textual (embeddings ou TF-IDF) entre o `termo_local`
e os nomes/descrições dos IDs canônicos. Sugere os top-3 candidatos com
score. **Nunca inventa** — apenas rankeia IDs que existem no catálogo.
`metodo = similaridade`, `confianca_ia` conforme o score.

### Camada 3 — Match por LLM restrito (IA generativa, controlada)
Só quando 1 e 2 não resolvem. A regra de ouro: **o LLM só pode escolher
entre os IDs canônicos que existem.** O prompt entrega a lista de
candidatos e pede "qual destes, ou nenhum". Se "nenhum", vai para fila de
revisão humana. `metodo = llm`.

**O LLM nunca cria um `canonico_id`.** A validação rejeita qualquer
`canonico_id` que não exista no catálogo. Isso elimina alucinação por
construção: o pior caso é "não sei" (fila humana), nunca "inventou um ID
errado que parece certo".

## O fluxo de uso

```
1. Banco entrega tabelas locais (qualquer formato, vocabulario proprio)
        ↓
2. Engine PROPOE o de-para → preenche B_MAP com status=sugerido
   (camada 1 → 2 → 3, com confianca e metodo por linha)
        ↓
3. Humano revisa:
   - aprova "alta confianca" em lote (com amostragem de conferencia)
   - revisa um a um "media" e "baixa"
   - ajusta ou rejeita o que estiver errado
        ↓
4. B_MAP aprovado vira a ponte permanente
        ↓
5. BooX traduz tabelas locais -> canonico e gera o 20-box
        ↓
6. Proximo ciclo: termos ja mapeados sao reusados (camada 1);
   so termos NOVOS passam pela engine
```

## Governança e auditabilidade

Cada linha do B_MAP registra **quem aprovou, quando, por qual método e com
qual justificativa**. Isso torna o de-para auditável — fundamental em
contexto regulatório, onde o RCSA é peça inspecionável. A IA acelera o
trabalho humano; ela nunca decide sozinha. O julgamento final é sempre de
uma pessoa identificada.

## Exemplo

```csv
id;dominio;termo_local;termo_local_id;canonico_id;confianca_ia;metodo;justificativa;status;aprovado_por;data_revisao;notas
MAP-001;segmento;Clientes Premium PF;SEG-04;ORG.NEG.ALT;alta;similaridade;Premium PF corresponde a alta renda;aprovado;Joao Silva;2026-01-15;
MAP-002;risco;Invasao de sistemas;RSC-22;R0.U.7;alta;llm;Invasao de sistemas e risco cibernetico;aprovado;Maria Souza;2026-01-15;
MAP-003;organizacao;DICOI;;ORG.CIN.CTI;media;llm;DICOI sugere Diretoria de Controles Internos;ajustado;Maria Souza;2026-01-16;Confirmado com a area
MAP-004;risco;Risco de granizo na lavoura;RSC-88;;baixa;llm;Nenhum canonico adequado;rejeitado;Joao Silva;2026-01-16;Risco muito especifico - tratar como subitem de socioambiental
```

(No MAP-004, a engine corretamente devolveu "nenhum" em vez de forçar um
mapeamento errado — o caso vai para decisão humana.)

## Relacionamento com os outros Books

O B_MAP é consultado pela engine **antes** de processar qualquer Book
local. Toda referência a um termo local nas tabelas do banco passa pelo
B_MAP para ser resolvida ao ID canônico, e só então entra no cálculo do
score e do 20-box.
