@echo off
setlocal
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m PyInstaller --noconfirm --clean --windowed --name WebAutomationBot --collect-all customtkinter main.py
if errorlevel 1 exit /b 1
echo Build complete: dist\WebAutomationBot.exe
