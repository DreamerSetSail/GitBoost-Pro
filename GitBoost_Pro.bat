@echo off
chcp 65001 >nul
title GitBoost Pro - All-in-One GitHub Accelerator

cd /d "%~dp0"

:: Check admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] Requesting administrator privileges...
    echo Please click "Yes" in the UAC dialog.
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cls
echo ============================================
echo   GitBoost Pro v2.0 - Administrator Mode
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

:: Run main program
python gitboost_pro_all_in_one.py
