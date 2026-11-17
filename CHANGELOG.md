# Changelog

Todas as mudanças notáveis do BooX são documentadas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).

## 1.11.8 - PATCH
- Promovidos a `ativo` 36 testes revisados pelo responsavel: Res. CVM 30, Res. CVM 161 e Regras e Procedimentos de Suitability da ANBIMA (Nº 01/2019, alteradas pelas Nº 06/21), todos de criticidade alta.
- Os demais testes dessas normas seguem `proposto`; os testes de exemplo TST.SEED.* (sem artigo citado) tambem.

## 1.11.7 - PATCH
- Promovidos a `ativo` 57 testes revisados pelo responsavel: Res. CVM 21, Res. CVM 32 (consolidada com a Res. CVM 209/24) e Res. CVM 33, todos de criticidade alta.
- Os demais testes dessas normas seguem `proposto`.

## 1.11.6 - PATCH
- Promovidos a `ativo` 36 testes da Res. CVM 35 (texto consolidado com as Res. CVM 134/22, 179/23 e 209/24; vigente a redacao dada pela Res. CVM 134/22 aos arts. 20, 21, 22, 31 e 49), revisados pelo responsavel.
- Os demais testes da CVM 35 seguem `proposto`.

## 1.11.5 - PATCH
- Promovidos a `ativo` 69 testes de criticidade alta revisados pelo responsavel: 54 da Res. CVM 175 (Parte Geral e Anexos I a IV) e 15 da Res. CNSP 416 (SUSEP).
- Testes de criticidade media e baixa dessas normas seguem `proposto`. Texto da CNSP 416 conferido na versao original; alteracoes posteriores nao verificadas.

## 1.11.4 - PATCH
- Promovidos a `ativo` 15 testes da Res. CMN 4.893 (texto consolidado vigente em 19/12/2025, com a Res. CMN 5.274/2025), revisados pelo responsavel.
- Os testes de exemplo TST.SEED.CYBER.* (sem artigo citado) permanecem `proposto`.

## 1.11.3 - PATCH
- Promovidos a `ativo` 56 testes revisados pelo responsavel (2a rodada): 23 da Circ. BCB 3.978, 16 da Res. CMN 4.557 e 17 da Res. CMN 4.968, de criticidade media e baixa.
- Com esta rodada, as tres normas centrais ficam integralmente validadas; o teste de exemplo TST.SEED.CONF.001 (sem artigo citado) permanece `proposto`.

## 1.11.2 - PATCH
- Promovidos a `ativo` 49 testes revisados pelo responsavel: 21 da Res. CMN 4.557 e 28 da Res. CMN 4.968 (todos de criticidade alta).
- Texto conferido contra a versao consolidada vigente (CMN 4.968 em 29/12/2025); dispositivos revogados do art. 5 da 4.968 (inc. IV 'i' e par. unico, Res. Conjunta 18/2025) nao sao citados por nenhum teste.
- Testes de criticidade media/baixa seguem `proposto`.

## [Não lançado]

#### Tipos de fundo administrados (canônico 1.11.0)
- Coluna opcional `tipos_fundo` em B_TESTES_canonico e enum `tipo_fundo` (fif, fidc, fii, fip); o gap aceita `tipos_fundo` (CLI `--tipos-fundo "a|b"`) e o app ganha o seletor "Tipos de fundo administrados" (vazio = todos). Sem declarar tipos de fundo, os números não mudam.

#### Aplicabilidade por atividade (canônico 1.9.0)
- Coluna opcional `atividades` em B_TESTES_canonico e enum `atividade`; o gap aceita `atividades` (CLI `--atividades "a|b"`) e o app ganha o seletor "Atividades exercidas". Sem declarar atividades, os números não mudam. O app avisa que a cobertura SUSEP é parcial (apenas CNSP 416).

#### Exemplo e catálogo (canônico 1.5.0)
- Base `banco_modelo_sa` atualizada: normas vigentes (CMN 4.893 no lugar da 4.658 revogada), 28 execuções de testes do catálogo novo e evidências coerentes.
- Catálogo canônico: 229 testes `proposto` (CVM 21, 30, 32, 33, 35, 161; ANBIMA suitability; CMN 4.893).

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

## [0.2.0] — 2026-11-13

### v0.2 — Mudancas metodologicas (bolhas-pizza + apontamentos no eixo X)

#### Mudado
- **Eixo X passa a usar apenas apontamentos + controles + cobertura.**
  KRIs e sinais externos saem do calculo direto do score. Tese: todo
  problema concreto deve virar apontamento (com plano de acao); KRIs e
  externos sao fontes POTENCIAIS de apontamento.
- **Cobertura entra como dimensao de primeira classe.** Cada par carrega
  percentual derivado de `status_validacao` dos controles
  (apenas_autoavaliado=25, doc=50, amostral=75, completo=100).
- **Bolhas viraram pizzas** no 20-box: preto = coberto, cinza = nao
  coberto. Contorno colorido = prioridade; tamanho = materialidade.

#### Adicionado
- **Alertas de descobertura**: KRIs vermelho/amarelo e externos relevantes
  sem apontamento associado viram "decisoes pendentes" listadas no 20-box
  e parecer. Forca decisao: abrir apontamento ou justificar.
- `detalhamento.csv` ganha coluna `cobertura_pct`.

### Fase 1 — Cadeia regulamentar (Processo → Risco → FR → Controle → Teste)

#### Adicionado
- **Cadeia hierarquica completa** em `docs/cadeia_regulamentar.md`
- **Extensao da taxonomia de riscos ate R4** (20 R1-R4 seed em 3 ramos:
  Cyber, Conformidade, PLD-FT) — total agora: 41 riscos canonicos
- **Book canonico `B_FR_canonico`** — 9 Fatores de Risco seed
- **Book canonico `B_TESTES_canonico`** — 7 testes seed marcados como
  `proposto` (arcabouco, nao conteudo regulatorio validado — Fase 2 traz
  piloto BSM PQO com fonte oficial rastreada)
- **Books locais** `B_TESTES_execucao` e `B_EVIDENCIA`
- **Engine `boox/gap_regulatorio.py`** — cobertura por regulador, gaps
  criticos, controles orfaos, FRs descobertos
- **Filtro por tipo de instituicao** (banco_multiplo, corretora, DTVM,
  seguradora, cooperativa...)
- Curador estendido com dominios `fatores` e `testes`
- Validador confere integridade das referencias (FR→risco, teste→FR,
  teste→risco)

## [0.2.1] — 2026-11-13

### Fase 2 piloto — BSM PQO 2025, Capitulo 1 (CADASTRAR CLIENTES)

#### Adicionado
- **14 testes canonicos ATIVOS** rastreados item-a-item ao Roteiro PQO BSM 2025,
  Capitulo 1 (TST.BSM.PQO.CAD.001 a 014) — primeiros testes do BooX com
  **conteudo regulatorio validado por fonte oficial**
- `docs/fase2_bsm_pqo.md` — metodologia de extracao (fidelidade vs
  interpretacao do mantenedor), codificacao de normas CVM, e roadmap
  dos demais capitulos
- Execucoes e evidencias BSM no Banco Modelo (`B_TESTES_execucao.csv` e
  `B_EVIDENCIA.csv`) demonstrando os quatro estados: conforme, parcial,
  nao conforme, sem execucao
- Gap regulatorio filtrado por tipo=corretora agora mostra 20 testes
  aplicaveis (14 BSM + 6 seeds) com cobertura por regulador

#### Status dos testes canonicos
- Ativos: 14 (todos BSM PQO Cap 1)
- Propostos: 7 (seeds Cyber, Conformidade, PLDFT — aguardando conversao
  em proximas iteracoes da Fase 2)

## [0.2.2] — 2026-11-13

### Empacotamento para uso profissional / corporativo

#### Adicionado
- `pyproject.toml` — pacote `boox-ro` instalavel com `pip install .`
- Entry points `boox` e `boox-gap` disponiveis globalmente apos instalacao
- `SECURITY.md` — documento para equipes de SI do banco: superficie de
  ataque, dependencias, o que o BooX faz e nao faz
- Flag `--air-gapped` na engine: intercepta `socket.connect` em runtime
  e alerta sobre proxies ativos (defesa em profundidade)
- `Dockerfile` + `.dockerignore` — imagem minima para rodar com
  `--network=none` (isolamento de rede provado pelo runtime)
- `requirements.txt` — documentacao de dependencias (openpyxl opcional
  para templates)
- Secao "Instalacao" e "Seguranca" no README

#### Mudado
- `boox/_campos.py` criado como copia canonica da spec de campos
- `schema/campos.py` virou shim de compatibilidade, re-exportando de
  `boox._campos` (necessario para o pacote funcionar quando instalado
  fora do diretorio do repositorio)
