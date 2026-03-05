@echo off
echo ============================================
echo    Construction de PDF Numeroteur
echo ============================================
echo.

:: Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR : Python n'est pas installe ou pas dans le PATH.
    echo Telechargez-le sur https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Créer un environnement virtuel
echo [1/4] Creation de l'environnement virtuel...
if not exist .venv (
    python -m venv .venv
)

:: Activer l'environnement virtuel
call .venv\Scripts\activate.bat

:: Installer les dépendances
echo [2/4] Installation des dependances...
pip install --quiet PyQt6 PyPDF2 reportlab pyinstaller pywin32 comtypes pillow

:: Compiler l'application
echo [3/4] Compilation de l'application...
pyinstaller build_windows.spec --noconfirm

:: Vérifier le résultat
echo.
if exist dist\PDF-Numeroteur.exe (
    echo [4/4] Compilation reussie !
    echo.
    echo L'executable se trouve dans :
    echo    %cd%\dist\PDF-Numeroteur.exe
    echo.
) else (
    echo ERREUR : La compilation a echoue.
    echo Verifiez les messages d'erreur ci-dessus.
)

pause
