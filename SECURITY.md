# Seguranca e privacidade no uso do BooX

Este documento descreve, para equipes de Seguranca da Informacao, o que
o BooX faz e o que ele nao faz com os dados do banco. E a base tecnica
para a analise de risco de fornecedor/ferramenta.

## Resumo executivo

- **Codigo open-source auditavel** (licenca MIT) — todo o codigo pode
  ser lido antes de rodar. Sem binarios opacos.
- **100% local** — a engine de calculo nao faz nenhuma chamada de rede.
  Nao telefona para casa.
- **Zero dependencias externas na engine** — `compute.py`, `render.py`,
  `suficiencia.py` e `gap_regulatorio.py` usam apenas a biblioteca
  padrao do Python. Nada precisa ser baixado para operar.
- **Dados ficam dentro do perimetro do banco** — os Books sao CSVs
  locais; nenhum deles e enviado para fora.

## O que o BooX faz

1. Le arquivos CSV locais (`B1_processos.csv`, `B5_controles.csv`, ...)
2. Calcula scores em memoria (Python puro, sem GPU, sem rede)
3. Escreve arquivos de saida locais: `20box.html`, `parecer.md`,
   `detalhamento.csv`, `suficiencia.md`, `gap_regulatorio.md`

## O que o BooX NAO faz

- Nao abre socket de rede
- Nao faz chamada HTTP/HTTPS
- Nao envia dados para APIs externas
- Nao usa LLM externo (OpenAI, Anthropic, Azure OpenAI, etc.)
- Nao armazena dados fora do diretorio de trabalho
- Nao instala servicos, daemons ou tarefas agendadas
- Nao requer privilegios administrativos
- Nao coleta telemetria
- Nao usa cookies, nao abre portas

## Superficie de ataque

### Dependencias

A engine de calculo tem **zero dependencias externas**. Verificavel por:

```bash
grep -r "^import\|^from" boox/*.py | grep -v "^boox/" | grep -oP "(?<=import |from )[\w.]+" | sort -u
```

Resultado esperado: apenas modulos da biblioteca padrao (`csv`, `os`,
`sys`, `math`, `colorsys`, `collections`).

O pacote opcional `openpyxl` (apenas para gerador de templates Excel) e
a unica dependencia externa, e pode ser omitido se a area nao usar os
templates.

### Instalacao

- `pip install boox-ro` (do PyPI) ou `pip install .` (do repo local)
- Instalado como pacote Python do usuario (sem root)
- Se o banco tem Artifactory/Nexus interno, instalar de la (recomendado)

### Execucao

- Rodar com o Python do usuario, sem venv-root
- Tempo de execucao: < 2s para a instancia de referencia (Banco Modelo)
- Memoria: < 50 MB

## Classificacao dos dados

Os Books contem informacoes classificadas como **confidenciais/internas**
pelo banco (apontamentos, controles, KRIs, apontamentos, riscos). Ou
seja, o BooX nao cria dados sensiveis — ele processa os que ja existem
no RCSA do banco.

Recomendacoes para o custodio dos arquivos:
- Guardar os CSVs em diretorio com controle de acesso (SharePoint
  corporativo, pasta com ACL, Git interno) — nunca em pasta publica
- Criptografia em repouso (ja deve existir na politica do banco)
- Trilha de auditoria de quem mexeu nos Books (Git interno resolve)

## Modo ar-gapped

Para ambientes com paranoia maxima de rede, a engine pode ser executada
em modo ar-gapped (opcao `--air-gapped`), que:
- Desabilita qualquer importacao de modulos opcionais que possam ter
  codigo de rede
- Verifica no inicio da execucao que nenhuma variavel de ambiente
  HTTP_PROXY/HTTPS_PROXY esta ativa
- Grava no log a confirmacao "modo ar-gapped ativo"

Exemplo:
```bash
python -m boox examples/banco_modelo_sa --out output --air-gapped
```

## Verificacao de integridade

Para garantir que o codigo nao foi alterado:

```bash
# No repositorio original
git log --oneline -5
git diff HEAD

# Hash SHA256 dos arquivos core
sha256sum boox/*.py canonico/*.py
```

O repositorio canonico e `https://github.com/walterCNeto/BooX`. Qualquer
divergencia deve ser investigada antes de rodar.

## Reporte de vulnerabilidade

Para reportar uma vulnerabilidade de seguranca, abrir issue privada no
repositorio ou contatar o mantenedor diretamente. Nao usar issues
publicas para questoes de seguranca.

## O que este documento NAO cobre

- **Politica interna do banco** sobre uso de ferramentas open-source —
  deve ser consultada separadamente
- **Classificacao dos dados do RCSA** — e responsabilidade do banco
- **Controles de acesso aos arquivos CSV** — e responsabilidade do banco
- **Validacao regulatoria do framework** — o BooX e uma ferramenta de
  apoio, nao substitui o framework de risco operacional do banco nem
  sua aprovacao pelo Comite de Risco
