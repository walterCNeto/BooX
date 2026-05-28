# B9 — Disciplinas

As disciplinas de risco do banco: as grandes áreas temáticas sob as quais
riscos, controles e indicadores se organizam transversalmente. Funcionam
como uma dimensão de corte independente da hierarquia de riscos.

## Disciplinas típicas

Crédito, Mercado, Liquidez, Taxas de Juros, Cobrança, Trabalhista, Modelo,
Operacional, Fiscal, Fraude, RSAC (responsabilidade socioambiental),
Reputacional, Concentração, BIA (continuidade), Tecnologia, LD (lavagem de
dinheiro), CF (combate ao financiamento), SI (segurança da informação),
Cyber, Fornecedores, Infraestrutura.

A casa pode adaptar a lista conforme sua taxonomia interna.

## Arquivo

`B9_disciplinas.csv`

## Colunas

| Coluna | Tipo | Obrig. | Descrição |
|--------|------|--------|-----------|
| `id` | string | sim | ID único (ex: `DISC_CREDITO`) |
| `nome` | string | sim | Nome da disciplina |
| `descricao` | string | não | Escopo da disciplina |
| `categoria_basileia` | string | não | Categoria Basileia associada |
| `responsavel_2linha` | string | não | Área de 2ª linha que monitora (ref. B12 ou livre) |

## Validações

- `id` único
- `nome` não vazio

## Papel no BooX

Disciplinas são uma **dimensão de agregação e filtro**:

- Riscos (B6) referenciam disciplina via `disciplina_id`
- Controles (B5) têm tipo que mapeia para disciplina
- Indicadores (B10) referenciam disciplina
- Sinais externos (B8) podem referenciar disciplina
- Visões (B7) podem filtrar por disciplina

Permitem perguntas como "como está o ambiente de controles da disciplina
Cyber em toda a casa?" — agregando todos os pares de riscos daquela
disciplina, independentemente do processo.

## Relacionamentos

- Referenciado por **B6** (riscos), **B8** (externos), **B10** (indicadores), **B7** (visões)

## Exemplo

```csv
id;nome;descricao;categoria_basileia;responsavel_2linha
DISC_CREDITO;Credito;Risco de credito em todas as carteiras;credito;Riscos de Credito
DISC_CYBER;Cyber;Seguranca cibernetica e resiliencia;operacional;Ciberseguranca
DISC_LGPD;Privacidade e LGPD;Protecao de dados pessoais;operacional;Privacidade e Dados
DISC_CONDUTA;Conduta;Conduta de mercado e suitability;operacional;Compliance
DISC_LD;Lavagem de Dinheiro;PLD-FT;operacional;PLD
```
