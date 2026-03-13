#!/bin/bash
#
# Todo Calendar - 打包脚本
# 使用 PyInstaller 打包为可执行文件
#
# 使用方法:
#   ./build.sh              # 打包当前平台
#   ./build.sh --clean      # 清理缓存后打包
#   ./build.sh --help       # 显示帮助
#

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# 虚拟环境 Python
VENV_PYTHON="${PROJECT_ROOT}/venv/bin/python"

# PyInstaller 规格文件
SPEC_FILE="${PROJECT_ROOT}/todo_calendar.spec"

# 输出目录
DIST_DIR="${PROJECT_ROOT}/dist"
BUILD_DIR="${PROJECT_ROOT}/build"

# 检查参数
CLEAN_BUILD=false
SHOW_HELP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN_BUILD=true
            shift
            ;;
        --help|-h)
            SHOW_HELP=true
            shift
            ;;
        *)
            echo -e "${RED}未知参数：$1${NC}"
            echo "使用 --help 查看帮助"
            exit 1
            ;;
    esac
done

# 显示帮助
if [ "$SHOW_HELP" = true ]; then
    echo "Todo Calendar 打包脚本"
    echo ""
    echo "使用方法:"
    echo "  ./build.sh              # 打包当前平台"
    echo "  ./build.sh --clean      # 清理缓存后打包"
    echo "  ./build.sh --help       # 显示帮助"
    echo ""
    echo "输出:"
    echo "  dist/todo_calendar      # Linux/macOS 可执行文件"
    echo "  dist/todo_calendar.exe  # Windows 可执行文件"
    exit 0
fi

# 检查虚拟环境
if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${RED}错误：虚拟环境未找到${NC}"
    echo "请先创建虚拟环境并安装依赖："
    echo "  python3 -m venv venv"
    echo "  ./venv/bin/pip install -r requirements.txt"
    exit 1
fi

# 检查 PyInstaller 是否安装
if ! "$VENV_PYTHON" -m pip show pyinstaller > /dev/null 2>&1; then
    echo -e "${YELLOW}PyInstaller 未安装，正在安装...${NC}"
    "$VENV_PYTHON" -m pip install pyinstaller>=6.0.0
fi

# 清理构建缓存
if [ "$CLEAN_BUILD" = true ]; then
    echo -e "${YELLOW}清理构建缓存...${NC}"
    rm -rf "$BUILD_DIR"
    rm -rf "$DIST_DIR"
    rm -f "$SPEC_FILE"
fi

# 创建必要的目录
mkdir -p "$DIST_DIR"

echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}Todo Calendar 打包开始${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""

# 显示系统信息
echo -e "${YELLOW}系统信息:${NC}"
echo "  项目目录：$PROJECT_ROOT"
echo "  Python: $($VENV_PYTHON --version)"
echo "  平台：$(uname -s) $(uname -m)"
echo ""

# 运行 PyInstaller
echo -e "${YELLOW}开始打包...${NC}"
"$VENV_PYTHON" -m PyInstaller \
    --clean \
    --noconfirm \
    "$SPEC_FILE"

# 检查打包结果
if [ -f "${DIST_DIR}/todo_calendar" ] || [ -f "${DIST_DIR}/todo_calendar.exe" ]; then
    echo ""
    echo -e "${GREEN}==================================${NC}"
    echo -e "${GREEN}✓ 打包成功！${NC}"
    echo -e "${GREEN}==================================${NC}"
    echo ""
    
    # 显示输出文件
    echo -e "${YELLOW}可执行文件位置:${NC}"
    if [ -f "${DIST_DIR}/todo_calendar" ]; then
        echo "  ${DIST_DIR}/todo_calendar"
        ls -lh "${DIST_DIR}/todo_calendar"
    elif [ -f "${DIST_DIR}/todo_calendar.exe" ]; then
        echo "  ${DIST_DIR}/todo_calendar.exe"
        ls -lh "${DIST_DIR}/todo_calendar.exe"
    fi
    
    echo ""
    echo -e "${YELLOW}测试运行:${NC}"
    echo "  ${DIST_DIR}/todo_calendar"
    echo ""
    
else
    echo ""
    echo -e "${RED}==================================${NC}"
    echo -e "${RED}✗ 打包失败${NC}"
    echo -e "${RED}==================================${NC}"
    echo ""
    echo "请检查构建日志以获取详细信息"
    exit 1
fi
