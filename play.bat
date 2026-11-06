@echo off
cd /d "%~dp0"
if exist "app\windows-latest\main_hub\main_hub.exe" (
    start "" "app\windows-latest\main_hub\main_hub.exe"
) else (
    python main_hub.py
)
