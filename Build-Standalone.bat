@echo off
setlocal
cd /d "%~dp0"
title Satella-Unlocked - Standalone Builder

where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo Python 3 is required to BUILD this app.
        echo Install it from https://www.python.org/downloads/
        pause
        exit /b 1
    )
    set "PYTHON_CMD=python"
)

echo Installing or upgrading PyInstaller...
%PYTHON_CMD% -m pip install --upgrade pyinstaller
if errorlevel 1 goto :error

echo Building standalone Satella-Unlocked.exe...
%PYTHON_CMD% -m PyInstaller --noconfirm --clean --onefile --windowed --name "Satella-Unlocked" "Satella-Unlocked.py"
if errorlevel 1 goto :error

echo.
echo Build complete: dist\Satella-Unlocked.exe
echo You can copy this EXE to Windows PCs without Python installed.
pause
exit /b 0

:error
echo.
echo Build failed. Check the error messages above.
pause
exit /b 1
