#!/usr/bin/env python3
"""
Archivo principal del programa.
Punto de entrada de la aplicación.
"""

import sys
import os

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import main

if __name__ == "__main__":
    main()
