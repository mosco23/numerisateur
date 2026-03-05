# PDF Numéroteur

Application cross-plateforme (Linux / Windows) pour numéroter, imprimer et numériser des pages.

## Fonctionnalités

- **Impression de numéros** : imprime des numéros de page en haut des feuilles (gauche, centre ou droite)
- **Numérisation automatique** : scanne les feuilles après impression et les sauvegarde dans un dossier
- **Numérotation de PDF existant** : ajoute des numéros de page à un fichier PDF
- **Plage configurable** : numéro de début et de fin au choix
- **Options** : taille de police, marge, position, format de sortie (PDF/PNG/JPEG), résolution (DPI)

## Installation

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install pywin32 comtypes pillow
python main.py
```

## Compiler en exécutable Windows

Double-cliquez sur `build_windows.bat` ou exécutez :

```bash
pip install pyinstaller pywin32 comtypes pillow
pyinstaller build_windows.spec --noconfirm
```

L'exécutable sera dans `dist\PDF-Numeroteur.exe`.

## Structure du projet

```
├── main.py                # Point d'entrée
├── requirements.txt       # Dépendances
├── build_windows.bat      # Script de compilation Windows
├── build_windows.spec     # Configuration PyInstaller
├── app/
│   ├── styles.py          # Feuille de style QSS
│   ├── utils.py           # Utilitaires UI
│   ├── platform_utils.py  # Impression/scan cross-plateforme
│   ├── workers.py         # Threads (scan, numérotation PDF)
│   ├── window.py          # Fenêtre principale
│   ├── tab_print.py       # Onglet Impression + Numérisation
│   └── tab_pdf.py         # Onglet PDF Existant
```

## Technologies

- **PyQt6** — Interface graphique
- **ReportLab** — Génération des numéros de page
- **PyPDF2** — Manipulation de fichiers PDF
- **SANE / WIA** — Numérisation (Linux / Windows)
