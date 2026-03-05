# PDF Numeroteur

Application PyQt6 pour imprimer des numeros sur des feuilles et les numeriser.

## Structure

- `main.py` — Point d'entree
- `app/window.py` — Fenetre principale (MainWindow)
- `app/tab_print.py` — Onglet unique : impression des numeros + numerisation
- `app/workers.py` — ScanWorker (thread de numerisation)
- `app/platform_utils.py` — Fonctions cross-plateforme (impression, scan SANE/WIA)
- `app/styles.py` — Feuille de style QSS
- `app/utils.py` — Utilitaires UI (ombres, labels)
- `build_windows.bat` — Script de compilation Windows (utilise `venv`, pas `.venv`)
- `build_windows.spec` — Configuration PyInstaller
- `installer.iss` — Inno Setup pour l'installeur Windows

## Conventions

- Python 3.12, PyQt6
- Interface en francais
- Impression directe via QPainter/QPrinter (pas de PDF intermediaire)
- Le numero est imprime 2 fois par page : en haut et au milieu (pour couper la feuille en deux)
- Position du numero configurable (Gauche/Centre/Droite), marge haut fixe a 15mm
- Scanner optionnel : mode impression seule si aucun scanner detecte

## Commandes

```bash
# Lancer l'application
python main.py

# Compilation Windows
build_windows.bat
```
