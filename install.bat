@echo off
REM Script de instalación para el Sistema de Diagnóstico Médico con Prolog
REM Windows PowerShell/CMD

echo ======================================================
echo   Sistema de Diagnóstico Médico - Instalación
echo   (Motor basado en Prolog)
echo ======================================================
echo.

REM Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH
    echo Descarga Python desde: https://www.python.org/
    pause
    exit /b 1
)
echo ✓ Python encontrado

REM Verificar SWI-Prolog
echo.
echo [2/5] Verificando SWI-Prolog...
swipl --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: SWI-Prolog no está instalado
    echo.
    echo Por favor instala SWI-Prolog:
    echo https://www.swi-prolog.org/download/stable
    echo.
    echo Asegúrate de:
    echo - Marcar "Add to PATH" durante la instalación
    echo - Reiniciar este script después de instalar
    pause
    exit /b 1
)
echo ✓ SWI-Prolog encontrado

REM Instalar pyswip
echo.
echo [3/5] Instalando pyswip...
pip install pyswip
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo instalar pyswip
    echo Intenta manualmente:
    echo python -m pip install --upgrade pyswip
    pause
    exit /b 1
)
echo ✓ pyswip instalado

REM Instalar pyautogui
echo.
echo [4/5] Instalando PyAutoGUI...
pip install pyautogui
if errorlevel 1 (
    echo.
    echo ERROR: No se pudo instalar PyAutoGUI
    echo Intenta manualmente:
    echo python -m pip install --upgrade pyautogui
    pause
    exit /b 1
)
echo ✓ PyAutoGUI instalado

REM Verificación final
echo.
echo [5/5] Verificando instalación...
python -c "from pyswip import Prolog; import pyautogui; print('✓ Prolog y PyAutoGUI listos')" >nul 2>&1
if errorlevel 1 (
    echo ERROR: No se pudo validar pyswip o PyAutoGUI
    echo Verifica la instalacion de SWI-Prolog y dependencias de Python
    pause
    exit /b 1
)
echo ✓ Integracion Prolog + RPA verificada

REM Éxito
echo.
echo ======================================================
echo ✓ INSTALACIÓN COMPLETADA
echo ======================================================
echo.
echo Para iniciar la aplicación, ejecuta:
echo   python Main.py
echo.
pause
