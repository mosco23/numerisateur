# -*- mode: python ; coding: utf-8 -*-
# Usage : pyinstaller build_windows.spec

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/logo.png', 'assets'),
        ('assets/logo.ico', 'assets'),
    ],
    hiddenimports=[
        'PyQt6', 'PyPDF2', 'reportlab',
        'comtypes', 'comtypes.client',
    ],
    hookspath=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PDF-Numeroteur',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon='assets/logo.ico',
)
