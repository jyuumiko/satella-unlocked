@echo off
setlocal
cd /d "%~dp0"

if exist "%~dp0Satella-Unlocked.exe" (
    "%~dp0Satella-Unlocked.exe" %*
    goto :done
)

where py >nul 2>nul
if not errorlevel 1 (
    py -3 "%~dp0Satella-Unlocked.py" %*
    goto :done
)

where python >nul 2>nul
if not errorlevel 1 (
    python "%~dp0Satella-Unlocked.py" %*
    goto :done
)

echo Python 3 was not found.
echo Install it from https://www.python.org/downloads/ and enable "Add Python to PATH".
pause
exit /b 1

:done
if errorlevel 1 (
    echo.
    echo The patcher returned an error.
    pause
) else (
    if not "%~1"=="" pause
)
endlocal
