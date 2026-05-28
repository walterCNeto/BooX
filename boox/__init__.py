# -*- coding: utf-8 -*-
"""BooX — Framework de Risco Operacional baseado em Books.

Uso rapido:
    python -m boox examples/banco_modelo_sa --out output
    python -m boox examples/banco_modelo_sa --out output --visao VIS_CONSIGNADO

API:
    from boox.compute import carregar
    inst = carregar("examples/banco_modelo_sa")
    res = inst.computar()   # lista de pares processo x risco com score e prioridade
"""
__version__ = "0.1.0"
__author__ = "Walter C. Neto"
__license__ = "MIT"
