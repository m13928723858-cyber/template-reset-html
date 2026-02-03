#!/bin/bash

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "  AI智能页面生成系统 - 快速启动"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查是否已经安装依赖
if [ ! -d "backend/venv" ]; then
    echo -e "${RED}[错误] 未检测到后端虚拟环境！${NC}"
    echo ""
    echo "请先运行 ./install-dependencies.sh 安装依赖"
    echo ""
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    echo -e "${RED}[错误] 未检测到前端依赖！${NC}"
    echo ""
    echo "请先运行 ./install-dependencies.sh 安装依赖"
    echo ""
    exit 1
fi

# 检查 .env 文件
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}[警告] 未找到 .env 文件！${NC}"
    echo ""
    echo "请确保已配置 DOLPHIN_API_KEY"
    echo "参考 backend/.env.example 创建 .env 文件"
    echo ""
    read -p "按回车继续，或按 Ctrl+C 取消..."
fi

echo -e "${BLUE}[1/3] 启动后端服务...${NC}"
echo ""

# 启动后端（新终端窗口）
osascript -e 'tell application "Terminal" to do script "cd '"$SCRIPT_DIR"'/backend && source venv/bin/activate && python main.py"'

# 等待后端启动
echo "等待后端服务启动..."
sleep 5

echo ""
echo -e "${BLUE}[2/3] 启动前端服务...${NC}"
echo ""

# 启动前端（新终端窗口）
osascript -e 'tell application "Terminal" to do script "cd '"$SCRIPT_DIR"'/frontend && npm run dev"'

# 等待前端启动
echo "等待前端服务启动..."
sleep 5

echo ""
echo -e "${BLUE}[3/3] 打开浏览器...${NC}"
echo ""
sleep 3
open http://localhost:5174

echo ""
echo "========================================"
echo -e "${GREEN}  ✅ 系统启动完成！${NC}"
echo "========================================"
echo ""
echo "📊 服务状态："
echo "  - 后端服务: http://localhost:8000"
echo "  - 前端服务: http://localhost:5174"
echo ""
echo "💡 使用说明："
echo "  1. 浏览器会自动打开前端页面"
echo "  2. 上传产品图片"
echo "  3. 填写产品信息"
echo "  4. 点击"生成页面"按钮"
echo "  5. 等待生成完成后下载"
echo ""
echo "🛑 停止服务："
echo "  - 关闭两个终端窗口即可停止服务"
echo "  - 或在窗口中按 Control+C 停止"
echo ""
echo "⚠️  注意事项："
echo "  - 请勿关闭后端和前端的终端窗口"
echo "  - 生成过程中请保持网络连接"
echo "  - 如遇问题请查看《使用手册-macOS.md》"
echo ""
echo "========================================"
echo ""
echo "按任意键关闭此窗口..."
read -n 1
