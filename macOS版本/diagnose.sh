#!/bin/bash

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "  系统诊断工具 (macOS版)"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查Python
echo -e "${BLUE}[1/8] 检查Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python3未安装${NC}"
    echo "  请访问: https://www.python.org/downloads/"
fi
echo ""

# 检查Node.js
echo -e "${BLUE}[2/8] 检查Node.js...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js未安装${NC}"
    echo "  请访问: https://nodejs.org/"
fi
echo ""

# 检查npm
echo -e "${BLUE}[3/8] 检查npm...${NC}"
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ npm $NPM_VERSION${NC}"
else
    echo -e "${RED}✗ npm未安装${NC}"
fi
echo ""

# 检查后端虚拟环境
echo -e "${BLUE}[4/8] 检查后端虚拟环境...${NC}"
if [ -d "backend/venv" ]; then
    echo -e "${GREEN}✓ 虚拟环境存在${NC}"
    
    # 检查依赖
    if [ -f "backend/venv/bin/python" ]; then
        echo "  检查Python依赖..."
        source backend/venv/bin/activate
        pip list | grep -E "fastapi|uvicorn|openai" > /dev/null
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}  ✓ 核心依赖已安装${NC}"
        else
            echo -e "${YELLOW}  ⚠ 部分依赖可能缺失${NC}"
        fi
        deactivate
    fi
else
    echo -e "${RED}✗ 虚拟环境不存在${NC}"
    echo "  请运行: ./install-dependencies.sh"
fi
echo ""

# 检查前端依赖
echo -e "${BLUE}[5/8] 检查前端依赖...${NC}"
if [ -d "frontend/node_modules" ]; then
    echo -e "${GREEN}✓ node_modules存在${NC}"
    
    # 检查关键依赖
    if [ -d "frontend/node_modules/react" ] && [ -d "frontend/node_modules/vite" ]; then
        echo -e "${GREEN}  ✓ 核心依赖已安装${NC}"
    else
        echo -e "${YELLOW}  ⚠ 部分依赖可能缺失${NC}"
    fi
else
    echo -e "${RED}✗ node_modules不存在${NC}"
    echo "  请运行: ./install-dependencies.sh"
fi
echo ""

# 检查配置文件
echo -e "${BLUE}[6/8] 检查配置文件...${NC}"
if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓ .env文件存在${NC}"
    
    # 检查API密钥
    if grep -q "DOLPHIN_API_KEY=sk-" backend/.env; then
        echo -e "${GREEN}  ✓ API密钥已配置${NC}"
    else
        echo -e "${YELLOW}  ⚠ API密钥可能未正确配置${NC}"
    fi
else
    echo -e "${RED}✗ .env文件不存在${NC}"
    echo "  请创建 backend/.env 文件"
fi
echo ""

# 检查端口占用
echo -e "${BLUE}[7/8] 检查端口占用...${NC}"

# 检查8000端口
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ 端口8000已被占用${NC}"
    echo "  进程: $(lsof -Pi :8000 -sTCP:LISTEN | tail -n 1 | awk '{print $1}')"
else
    echo -e "${GREEN}✓ 端口8000可用${NC}"
fi

# 检查5174端口
if lsof -Pi :5174 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ 端口5174已被占用${NC}"
    echo "  进程: $(lsof -Pi :5174 -sTCP:LISTEN | tail -n 1 | awk '{print $1}')"
else
    echo -e "${GREEN}✓ 端口5174可用${NC}"
fi
echo ""

# 检查网络连接
echo -e "${BLUE}[8/8] 检查网络连接...${NC}"
if ping -c 1 google.com &> /dev/null; then
    echo -e "${GREEN}✓ 网络连接正常${NC}"
else
    echo -e "${YELLOW}⚠ 网络连接可能有问题${NC}"
fi
echo ""

# 总结
echo "========================================"
echo -e "${BLUE}  诊断完成${NC}"
echo "========================================"
echo ""
echo "如果发现问题，请："
echo "  1. 根据上述提示修复"
echo "  2. 查看《使用手册-macOS.md》"
echo "  3. 联系技术支持"
echo ""
echo "按任意键退出..."
read -n 1
