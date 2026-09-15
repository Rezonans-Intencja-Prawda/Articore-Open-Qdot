# conftest.py — konfiguracja testów ArtiCore
import sys
import os

# Dodaj katalog repozytorium do ścieżki, aby `import core` działał
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
