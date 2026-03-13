@echo off
:: 【关键修复 1】强制设置控制台编码为 UTF-8 (代码页 65001)
chcp 65001 >nul

:: 【关键修复 2】强制 Python 使用 UTF-8 输出
set PYTHONIOENCODING=utf-8

title GitBoost Pro - Auto Language Detection
color 0A

:: 1. 检查管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :ADMIN
) else (
    echo [Info] Requesting administrator privileges...
    echo If a popup appears, please click "Yes".
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:ADMIN
cd /d "%~dp0"

echo ==========================================
echo    GitBoost Pro (Administrator Mode)
echo ==========================================
echo.

:: 2. 检查 Python 环境
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [Critical Error] Python is not detected!
    echo.
    echo Solution:
    echo 1. Download Python: https://www.python.org/
    echo 2. Install and CHECK "Add Python to PATH"
    echo.
    goto :WAIT_EXIT
)

echo [Info] Python detected. Starting GitBoost Pro...
echo.

:: 3. 运行 Python 脚本
python gitboost_pro.py

:: 4. 检查结果
if %errorLevel% neq 0 (
    echo.
    echo [Warning] Script finished with error code: %errorLevel%
)

:WAIT_EXIT
echo.
echo ------------------------------------------
echo Press any key to close...
pause >nul