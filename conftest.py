"""Asegura que la raíz del proyecto esté en sys.path para importar el paquete src en los tests."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
