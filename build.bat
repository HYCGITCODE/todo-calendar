@echo off
REM
REM Todo Calendar - Windows 打包脚本
REM 使用 PyInstaller 打包为可执行文件
REM
REM 使用方法:
REM   build.bat              # 打包
REM   build.bat --clean      # 清理缓存后打包
REM   build.bat --help       # 显示帮助
REM

setlocal enabledelayedexpansion

REM 项目根目录
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

REM 虚拟环境 Python
set "VENV_PYTHON=%PROJECT_ROOT%venv\Scripts\python.exe"

REM 检查参数
set "CLEAN_BUILD=false"
set "SHOW_HELP=false"

if "%1"=="--clean" set "CLEAN_BUILD=true"
if "%1"=="-h" set "SHOW_HELP=true"
if "%1"=="--help" set "SHOW_HELP=true"

REM 显示帮助
if "%SHOW_HELP%"=="true" (
    echo Todo Calendar 打包脚本 (Windows)
    echo.
    echo 使用方法:
    echo   build.bat              # 打包
    echo   build.bat --clean      # 清理缓存后打包
    echo   build.bat --help       # 显示帮助
    echo.
    echo 输出:
    echo   dist\todo_calendar.exe  # Windows 可执行文件
    exit /b 0
)

REM 检查虚拟环境
if not exist "%VENV_PYTHON%" (
    echo [错误] 虚拟环境未找到
    echo 请先创建虚拟环境并安装依赖:
    echo   python -m venv venv
    echo   venv\Scripts\pip install -r requirements.txt
    exit /b 1
)

REM 检查 PyInstaller 是否安装
"%VENV_PYTHON%" -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [警告] PyInstaller 未安装，正在安装...
    "%VENV_PYTHON%" -m pip install pyinstaller>=6.0.0
)

REM 清理构建缓存
if "%CLEAN_BUILD%"=="true" (
    echo [信息] 清理构建缓存...
    if exist "build" rmdir /s /q "build"
    if exist "dist" rmdir /s /q "dist"
    if exist "todo_calendar.spec" del /q "todo_calendar.spec"
)

REM 创建必要的目录
if not exist "dist" mkdir "dist"

echo ==================================
echo Todo Calendar 打包开始 (Windows)
echo ==================================
echo.

REM 显示系统信息
echo [信息] 系统信息:
echo   项目目录：%PROJECT_ROOT%
%VENV_PYTHON% --version
echo   平台：Windows
echo.

REM 运行 PyInstaller
echo [信息] 开始打包...
"%VENV_PYTHON%" -m PyInstaller ^
    --clean ^
    --noconfirm ^
    todo_calendar.spec

REM 检查打包结果
if exist "dist\todo_calendar.exe" (
    echo.
    echo ==================================
    echo [成功] 打包成功！
    echo ==================================
    echo.
    echo [信息] 可执行文件位置:
    echo   dist\todo_calendar.exe
    dir "dist\todo_calendar.exe"
    echo.
    echo [信息] 测试运行:
    echo   dist\todo_calendar.exe
    echo.
) else (
    echo.
    echo ==================================
    echo [失败] 打包失败
    echo ==================================
    echo.
    echo 请检查构建日志以获取详细信息
    exit /b 1
)

endlocal
