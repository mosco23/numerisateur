@echo off
echo ============================================
echo    Construction de PDF Numeroteur
echo ============================================
echo.

:: Verifier que Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR : Python n'est pas installe ou pas dans le PATH.
    echo Telechargez-le sur https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Creer un environnement virtuel
echo [1/5] Creation de l'environnement virtuel...
if not exist venv (
    python -m venv venv
)

:: Activer l'environnement virtuel
call venv\Scripts\activate.bat

:: Installer les dependances
echo [2/5] Installation des dependances...
pip install --quiet PyQt6 PyPDF2 reportlab pyinstaller comtypes pillow

:: Compiler l'application
echo [3/5] Compilation de l'application...
pyinstaller build_windows.spec --noconfirm

:: Verifier le resultat
echo.
if not exist dist\PDF-Numeroteur.exe (
    echo ERREUR : La compilation a echoue.
    echo Verifiez les messages d'erreur ci-dessus.
    pause
    exit /b 1
)

echo [4/5] Executable cree : dist\PDF-Numeroteur.exe

:: Generer l'installeur si Inno Setup est disponible
set ISCC_PATH=
where iscc >nul 2>&1
if not errorlevel 1 (
    set ISCC_PATH=iscc
) else if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
)

if defined ISCC_PATH (
    echo [5/5] Generation de l'installeur Windows...
    "%ISCC_PATH%" installer.iss
    echo.
    if exist installer_output\PDF-Numeroteur-Setup.exe (
        echo Installeur cree : installer_output\PDF-Numeroteur-Setup.exe
    ) else (
        echo AVERTISSEMENT : La generation de l'installeur a echoue.
    )
) else (
    echo [5/5] Inno Setup non detecte, installeur non genere.
    echo      Pour creer l'installeur, installez Inno Setup 6 :
    echo      https://jrsoftware.org/isdl.php
    echo      Puis relancez ce script.
)

echo.
echo ============================================
echo    Construction terminee !
echo ============================================
pause
