@echo off
:: ─────────────  Self-elevate to Administrator  ─────────────
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges…
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

:: ─────────────  Add the folder exclusion  ─────────────
cd /d "%~dp0"
echo.
echo Adding "%CD%" to Windows Defender exclusions…
powershell -Command "Add-MpPreference -ExclusionPath '%CD%'"
echo.
echo SUCCESS – this folder is now excluded.
pause
