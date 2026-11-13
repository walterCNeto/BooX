# -*- coding: utf-8 -*-
"""Compat shim — a fonte agora e boox/_campos.py.
Mantido aqui para scripts antigos que faziam `sys.path.insert('schema'); import campos`.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from boox._campos import *  # noqa
from boox._campos import BOOKS, ENUM  # explicitos
