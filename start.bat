@echo off
REM Todo Calendar - Launch Script
REM This script launches the Todo Calendar application

REM Change to the directory where this script is located
cd /d "%~dp0"

REM Launch the application
if exist "Todo Calendar.exe" (
    start "" "Todo Calendar.exe"
) else (
    echo ERROR: Todo Calendar.exe not found!
    echo Please run build.bat first to create the executable.
    pause
)
