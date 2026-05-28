# Changelog

Todas as mudanças notáveis do BooX são documentadas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).

## [Não lançado]

### Fase 1 — Especificação (em andamento)

#### Adicionado
- README do projeto com visão geral, 20-box e os 13 Books
- Licenças MIT (código) e CC BY 4.0 (dados)
- Especificação compacta dos 9 Books do BooX Lite (B1, B2, B4, B5, B6, B7, B8, B9, B10)
- Documento de metodologia: score de Impacto (eixo Y), score de Ambiente
  de Controles (eixo X), classificação de Prioridade de Tratamento, e
  fundamentação da escolha Impacto × Ambiente (não Probabilidade)
- Estrutura inicial do repositório

#### Planejado para as próximas fases
- Fase 2: Banco Modelo S.A. — 9 Books preenchidos com dados realistas
- Fase 2: Templates Excel de cada Book
- Fase 3: Biblioteca `boox` (load, validate, compute, render)
- Fase 3: CLI `boox run`
- Fase 4: Geração do 20-box HTML interativo
- Futuro: Books B3, B11, B12, B13; frontend web; banco de dados

### Templates Excel + Analise de Suficiencia

#### Adicionado
- 13 templates Excel (`templates/*.xlsx`), um por Book, com:
  - Campos coloridos por categoria (obrigatorio/recomendado/opcional)
  - Listas suspensas (data validation) nos campos enumerados
  - Comentarios com a dica de cada campo
  - Aba de instrucoes com a tabela de campos e legenda
- Especificacao unica de campos em `schema/campos.py` (fonte da verdade dos
  121 campos dos 13 Books, com categoria e tipo)
- Modulo `boox/suficiencia.py` — analise de suficiencia que diagnostica,
  por Book: % de preenchimento dos obrigatorios e recomendados, status
  (completo / valido-baixa-confianca / incompleto / ausente) e alertas
  estruturais cruzados (hierarquia, de-para, 5W2H incompleto, series curtas)
- `python -m boox` agora gera tambem `suficiencia.md`

#### Alterado
- B2 (Apontamentos): area_afetada e area_gestora agora OBRIGATORIAS (o risco
  materializado tem dono e responsavel); adicionados recorrencia e valor_perda
- B6 (Vinculo): enxugado para o mundo inerente (sem afetada/gestora — estas
  vivem no apontamento). Area do par no inerente = area dona do processo (B1)
- B1 (Processos): area_responsavel agora OBRIGATORIA; adicionados data_revisao,
  frequencia_execucao, volume_transacional
- B8: ampliado para incluir Ouvidoria e SAC alem dos sinais externos publicos
- Banco Modelo S.A. regenerado com todos os campos novos

### Curadoria do canonico (Rota A)

#### Adicionado
- Campos de governanca `status` (ativo/deprecado) e `substituido_por` em
  todos os CSVs canonicos
- `canonico/VERSION` (versionamento semantico, inicia em 1.0.0) e
  `canonico/CHANGELOG.md`
- `canonico/REGRAS.md` — regras de curadoria (aditivo livre, destrutivo
  proibido, deprecar em vez de apagar)
- `canonico/curar.py` — ferramenta de curadoria (adicionar/renomear/deprecar)
  com bump de versao e changelog automaticos; bloqueia reuso de IDs
- `canonico/validar.py` — validacao de integridade do canonico
- Analise de suficiencia agora detecta de-paras apontando para IDs
  canonicos deprecados ou inexistentes
