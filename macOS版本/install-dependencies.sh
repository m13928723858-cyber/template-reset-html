#!/bin/bash

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "  AI智能页面生成系统 - 依赖安装"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查Python
echo -e "${BLUE}[1/4] 检查Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[错误] 未检测到Python3！${NC}"
    echo ""
    echo "请先安装Python 3.8或更高版本："
    echo "https://www.python.org/downloads/"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python版本: $PYTHON_VERSION${NC}"
echo ""

# 检查Node.js
echo -e "${BLUE}[2/4] 检查Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}[错误] 未检测到Node.js！${NC}"
    echo ""
    echo "请先安装Node.js 16或更高版本："
    echo "https://nodejs.org/"
    echo ""
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node.js版本: $NODE_VERSION${NC}"
echo ""

# 安装后端依赖
echo -e "${BLUE}[3/4] 安装后端依赖...${NC}"
echo ""

cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] 虚拟环境创建失败！${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ 虚拟环境创建成功${NC}"
else
    echo -e "${YELLOW}虚拟环境已存在，跳过创建${NC}"
fi

# 激活虚拟环境并安装依赖
echo "安装Python依赖包..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}[错误] Python依赖安装失败！${NC}"
    deactivate
    exit 1
fi

echo -e "${GREEN}✓ 后端依赖安装成功${NC}"
deactivate
cd ..
echo ""

# 安装前端依赖
echo -e "${BLUE}[4/4] 安装前端依赖...${NC}"
echo ""

cd frontend

# 检查npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}[错误] npm未找到！${NC}"
    exit 1
fi

echo "安装Node.js依赖包..."
npm install

if [ $? -ne 0 ]; then
    echo -e "${RED}[错误] 前端依赖安装失败！${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 前端依赖安装成功${NC}"
cd ..
echo ""

# 检查.env文件
echo -e "${BLUE}检查配置文件...${NC}"
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}[警告] 未找到.env文件${NC}"
    echo ""
    echo "请创建 backend/.env 文件并配置API密钥："
    echo "  DOLPHIN_API_KEY=你的API密钥"
    echo ""
else
    echo -e "${GREEN}✓ 配置文件存在${NC}"
fi
echo ""

# 完成
echo "========================================"
echo -e "${GREEN}  ✅ 所有依赖安装完成！${NC}"
echo "========================================"
echo ""
echo "下一步："
echo "  1. 配置 backend/.env 文件（如果还没配置）"
echo "  2. 运行 ./start-services.sh 启动系统"
echo ""
echo "按任意键退出..."
read -n 1
