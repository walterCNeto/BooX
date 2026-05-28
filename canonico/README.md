# Camada Canônica do BooX

Esta pasta contém a **taxonomia canônica fixa** do BooX — o esqueleto
genérico que vale para qualquer banco comercial brasileiro. É a Camada
Canônica: nunca muda entre instituições.

Cada banco conecta seu vocabulário próprio a esta camada através do
**B_MAP** (de-para), descrito em [`../schema/books/b_map.md`](../schema/books/b_map.md).

## Princípio: conceito, nunca marca

A camada canônica usa apenas **conceitos genéricos**, nunca marcas de
banco. "Alta Renda" é canônico; "Personnalité", "Prime" e "Uniclass" são
marcas locais que cada banco mapeia para `ORG.NEG.ALT` via B_MAP. Assim
bancos diferentes conversam pelo mesmo vocabulário comum.

Fundamentação: a taxonomia de risco segue o arcabouço regulatório
brasileiro (Res. CMN 4.557, Res. BCB 54) e reflete a estrutura típica de
bancos comerciais brasileiros observada em relatórios públicos de Pilar 3.

## Arquivos

| Arquivo | Conteúdo |
|---------|----------|
| `B_ORG_dominios.csv` | 13 domínios organizacionais (diretorias) com linha de defesa |
| `B_ORG_areas.csv` | ~73 áreas funcionais dentro dos domínios |
| `B6_riscos_canonico.csv` | 20 riscos R0 canônicos (ancorados no Pilar 3) |
| `B9_disciplinas_canonico.csv` | 21 disciplinas de risco transversais |

## As três linhas de defesa

Os domínios organizacionais são marcados por linha de defesa, conforme o
modelo regulatório brasileiro:

- **1ª linha**: áreas que executam e são donas dos riscos (Negócios,
  Crédito, Tecnologia, Operações, Tesouraria)
- **2ª linha**: funções independentes de risco e conformidade (Riscos,
  Controles Internos e Compliance, Jurídico)
- **3ª linha**: avaliação independente (Auditoria Interna) e funções de
  apoio/suporte (Financeiro, Ouvidoria, RH, Fornecedores)

## Duplicação consciente (operação × governança)

Alguns temas aparecem em mais de um domínio de propósito — porque a
**operação** de um tema mora numa área e a **governança** mora em outra:

| Tema | Operação (faz) | Governança (define/monitora) |
|------|----------------|------------------------------|
| Segurança da Informação | ORG.TEC.SI | ORG.CIN.SEG |
| PLD-FT | ORG.TEC.PCF (sistemas) | ORG.CIN.PLD (função) |
| Câmbio | ORG.OPE.CAM (operação) | ORG.NEG.CEX (negócio) |

Isso reflete a distinção **afetada × gestora** do BooX: quem opera e quem
responde pela governança do controle podem ser áreas diferentes.

## Extensibilidade

A camada canônica é **2 níveis** (Domínio › Área) na v0.1. Pode ser
estendida para um 3º nível (subárea) sem quebrar nada — os IDs seguem
hierarquia por prefixo (`ORG.TEC.SI.SOC` seria uma subárea de SI).

Da mesma forma, os riscos R0 podem ganhar R1, R2... conforme a casa
detalha sua taxonomia, sempre ancorados nos 20 R0 canônicos.

## Curadoria do canonico (Rota A)

O canonico e **estavel mas evolutivo**. As regras completas estao em
[`REGRAS.md`](REGRAS.md). Em resumo: **aditivo e livre, destrutivo e
proibido, deprecar em vez de apagar**. IDs nunca sao apagados nem
reutilizados.

### Versionamento

O canonico tem versao semantica em [`VERSION`](VERSION) e historico em
[`CHANGELOG.md`](CHANGELOG.md):
- PATCH: correcao de rotulo/descricao
- MINOR: adicao de novos IDs (seguro)
- MAJOR: deprecacao de IDs em uso

### Ferramentas

```bash
# listar o conteudo de um arquivo canonico
python canonico/curar.py listar riscos

# adicionar um conceito novo (bump MINOR automatico)
python canonico/curar.py adicionar riscos --id R0.U.21 --nome "Risco de IA Generativa" \
   --campos categoria_basileia=operacional grupo=operacional descricao="..."

# renomear o rotulo de um ID (bump PATCH)
python canonico/curar.py renomear riscos --id R0.U.21 --nome "Risco de IA"

# deprecar um ID sem apagar (bump MAJOR; aponta o substituto)
python canonico/curar.py deprecar riscos --id R0.U.21 --substituido_por R0.U.6

# validar a integridade do canonico (sempre apos curar)
python canonico/validar.py
```

Dominios validos para curar/listar: `dominios`, `areas`, `riscos`, `disciplinas`.

### Campos de governanca

Cada registro canonico tem `status` (ativo/deprecado) e `substituido_por`.
A analise de suficiencia avisa quando um de-para (B_MAP) aponta para um ID
canonico deprecado ou inexistente, permitindo migracao gradual sem quebra.
