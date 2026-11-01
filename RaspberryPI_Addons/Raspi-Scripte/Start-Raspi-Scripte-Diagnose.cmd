@echo off
setlocal
set "RSP_STARTER=%LOCALAPPDATA%\Raspi-Scripte\Content\Assets\Start-Raspi-Scripte-Diagnose.ps1"
if not exist "%RSP_STARTER%" (
  echo Bitte zuerst den Inhaltsupdate auf 1.1.3.8 installieren.
  pause
  exit /b 1
)
powershell.exe -NoProfile -STA -WindowStyle Hidden -ExecutionPolicy Bypass -File "%RSP_STARTER%"
