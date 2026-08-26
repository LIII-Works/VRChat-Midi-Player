@echo off
setlocal
cd /d "%~dp0"

echo Installing or checking required Python packages...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Dependency setup failed. Please install Python 3.10 or newer.
    pause
    exit /b 1
)

echo.
echo Starting VRChat MIDI Player...
python midi_osc_player.py
if errorlevel 1 (
    echo.
    echo The player stopped because of an error.
    pause
)
endlocal
