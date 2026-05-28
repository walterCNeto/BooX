"""
BooX — Framework de Risco Operacional baseado em Books.

Este pacote (em construção na Fase 3) fornecerá:

    boox.load(path)      -> carrega os Books de um diretório
    instance.validate()  -> valida schema e integridade referencial
    instance.compute()   -> calcula score X (ambiente) e Y (impacto)
    instance.view(...)    -> aplica filtros de uma Visão (B7)
    view.render(...)     -> gera 20-box, parecer e detalhamento

Versão atual: v0.1 (Lite) — especificação e metodologia definidas em
schema/ e docs/. Implementação da biblioteca em andamento.

Ver README.md para visão geral e docs/metodologia.md para a formulação
do score.
"""

__version__ = "0.1.0.dev0"
__author__ = "Walter C. Neto"
__license__ = "MIT"
