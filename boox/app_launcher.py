# -*- coding: utf-8 -*-
"""Launcher do app Streamlit — expoe `boox-app` como comando.

Equivalente a: streamlit run boox/app_streamlit.py
"""
import sys, os, subprocess
from pathlib import Path

def main():
    app_path = Path(__file__).resolve().parent / "app_streamlit.py"
    if not app_path.exists():
        print(f"ERRO: arquivo nao encontrado: {app_path}")
        sys.exit(1)
    try:
        import streamlit  # noqa
    except ImportError:
        print("ERRO: streamlit nao esta instalado. Rode: pip install 'boox-ro[app]'")
        sys.exit(1)
    cmd = [sys.executable, "-m", "streamlit", "run", str(app_path)] + sys.argv[1:]
    sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
