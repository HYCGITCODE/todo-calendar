@echo off
REM
REM Todo Calendar - Windows 打包脚本
REM 使用 PyInstaller 打包为单文件可执行文件
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

REM 检查参数
set "CLEAN_BUILD=false"
set "SHOW_HELP=false"
set "USE_VENV=true"

if "%1"=="--clean" set "CLEAN_BUILD=true"
if "%1"=="-h" set "SHOW_HELP=true"
if "%1"=="--help" set "SHOW_HELP=true"
if "%1"=="--system" set "USE_VENV=false"

REM 显示帮助
if "%SHOW_HELP%"=="true" (
    echo Todo Calendar 打包脚本 (Windows)
    echo.
    echo 使用方法:
    echo   build.bat              # 使用虚拟环境打包
    echo   build.bat --clean      # 清理缓存后打包
    echo   build.bat --system     # 使用系统 Python 打包
    echo   build.bat --help       # 显示帮助
    echo.
    echo 输出:
    echo   dist\Todo Calendar.exe  # Windows 可执行文件
    exit /b 0
)

REM 设置 Python 命令
if "%USE_VENV%"=="true" (
    set "PYTHON_CMD=%PROJECT_ROOT%venv\Scripts\python.exe"
    
    REM 检查虚拟环境
    if not exist "%PYTHON_CMD%" (
        echo [错误] 虚拟环境未找到
        echo.
        echo 请先创建虚拟环境并安装依赖:
        echo   python -m venv venv
        echo   venv\Scripts\activate
        echo   pip install -r requirements.txt
        echo.
        echo 或者使用系统 Python:
        echo   build.bat --system
        exit /b 1
    )
) else (
    set "PYTHON_CMD=python"
)

REM 检查 PyInstaller 是否安装
"%PYTHON_CMD%" -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [警告] PyInstaller 未安装，正在安装...
    "%PYTHON_CMD%" -m pip install pyinstaller>=6.0.0
)

REM 清理构建缓存
if "%CLEAN_BUILD%"=="true" (
    echo [信息] 清理构建缓存...
    if exist "build" rmdir /s /q "build"
    if exist "dist" rmdir /s /q "dist"
    echo [信息] 缓存已清理
    echo.
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
"%PYTHON_CMD%" --version
echo   PyInstaller 版本:
"%PYTHON_CMD%" -m pip show pyinstaller | findstr Version
echo.

REM 运行 PyInstaller
echo [信息] 开始打包...
echo   使用 spec 文件：todo_calendar_single.spec
echo.

"%PYTHON_CMD%" -m PyInstaller ^
    --clean ^
    --noconfirm ^
    todo_calendar_single.spec

REM 检查打包结果
if exist "dist\Todo Calendar.exe" (
    echo.
    echo ==================================
    echo [成功] 打包成功！
    echo ==================================
    echo.
    echo [信息] 可执行文件位置:
    echo   dist\Todo Calendar.exe
    dir "dist\Todo Calendar.exe"
    echo.
    echo [信息] 文件大小:
    for %%A in ("dist\Todo Calendar.exe") do echo   %%~zA bytes
    echo.
    echo [信息] 测试运行:
    echo   dist\Todo Calendar.exe
    echo.
    echo [信息] 创建启动脚本...
    (
        echo @echo off
        echo cd /d "%%~dp0"
        echo "Todo Calendar.exe"
    ) > "dist\start.bat"
    echo   dist\start.bat 已创建
    echo.
) else if exist "dist\todo_calendar.exe" (
    echo.
    echo ==================================
    echo [成功] 打包成功！
    echo ==================================
    echo.
    echo [信息] 可执行文件位置:
    echo   dist\todo_calendar.exe
    dir "dist\todo_calendar.exe"
    echo.
) else (
    echo.
    echo ==================================
    echo [失败] 打包失败
    echo ==================================
    echo.
    echo 请检查以下可能的问题:
    echo   1. Python 版本是否为 3.8+
    echo   2. 依赖是否已安装：pip install -r requirements.txt
    echo   3. 查看 PyInstaller 输出日志
    echo.
    echo 常见错误:
    echo   - 缺少 PyQt6: pip install PyQt6
    echo   - 缺少 SQLAlchemy: pip install SQLAlchemy
    echo   - 缺少 python-dateutil: pip install python-dateutil
    echo.
    exit /b 1
)

endlocal
