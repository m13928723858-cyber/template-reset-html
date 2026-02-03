@echo off
chcp 65001 >nul
echo ========================================
echo   AI智能页面生成系统 - 依赖安装脚本
echo ========================================
echo.

REM 检查Python
echo [1/4] 检查Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python已安装
python --version
echo.

REM 检查Node.js
echo [2/4] 检查Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Node.js
    echo 请先安装Node.js 16或更高版本
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js已安装
node --version
echo.

REM 安装后端依赖
echo [3/4] 安装后端依赖...
echo 这可能需要几分钟，请耐心等待...
cd /d "%~dp0backend"

REM 创建虚拟环境
if not exist "venv" (
    echo 创建Python虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败
        pause
        exit /b 1
    )
)

REM 激活虚拟环境并安装依赖
echo 安装Python依赖包...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 安装后端依赖失败
    pause
    exit /b 1
)
echo ✅ 后端依赖安装完成
echo.

REM 安装前端依赖
echo [4/4] 安装前端依赖...
echo 这可能需要几分钟，请耐心等待...
cd /d "%~dp0frontend"
call npm install
if errorlevel 1 (
    echo ❌ 安装前端依赖失败
    pause
    exit /b 1
)
echo ✅ 前端依赖安装完成
echo.

REM 完成
echo ========================================
echo   ✅ 所有依赖安装完成！
echo ========================================
echo.
echo 下一步：
echo 1. 配置 backend\.env 文件（填写API密钥）
echo 2. 双击运行 start-services.bat 启动系统
echo.
pause
