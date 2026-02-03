@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    AI智能页面生成系统 - 快速启动
echo ========================================
echo.

REM 检查是否已经安装依赖
if not exist "backend\venv\Scripts\python.exe" (
    echo [错误] 未检测到后端虚拟环境！
    echo.
    echo 请先运行 install-dependencies.bat 安装依赖
    echo.
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo [错误] 未检测到前端依赖！
    echo.
    echo 请先运行 install-dependencies.bat 安装依赖
    echo.
    pause
    exit /b 1
)

REM 检查 .env 文件
if not exist "backend\.env" (
    echo [警告] 未找到 .env 文件！
    echo.
    echo 请确保已配置 DOLPHIN_API_KEY
    echo 参考 backend\.env.example 创建 .env 文件
    echo.
    pause
)

echo [1/3] 启动后端服务...
echo.
start "AI页面生成系统 - 后端服务" cmd /k "cd /d "%~dp0backend" && venv\Scripts\python.exe main.py"

REM 等待后端启动
echo 等待后端服务启动...
timeout /t 5 /nobreak >nul

echo.
echo [2/3] 启动前端服务...
echo.
start "AI页面生成系统 - 前端服务" cmd /k "cd /d "%~dp0frontend" && npm run dev"

REM 等待前端启动
echo 等待前端服务启动...
timeout /t 5 /nobreak >nul

echo.
echo [3/3] 打开浏览器...
echo.
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo ========================================
echo    ✅ 系统启动完成！
echo ========================================
echo.
echo 📊 服务状态：
echo   - 后端服务: http://localhost:8000
echo   - 前端服务: http://localhost:5173
echo.
echo 💡 使用说明：
echo   1. 浏览器会自动打开前端页面
echo   2. 上传产品图片
echo   3. 填写产品信息
echo   4. 点击"生成页面"按钮
echo   5. 等待生成完成后下载
echo.
echo 🛑 停止服务：
echo   - 关闭两个命令行窗口即可停止服务
echo   - 或在窗口中按 Ctrl+C 停止
echo.
echo ⚠️  注意事项：
echo   - 请勿关闭后端和前端的命令行窗口
echo   - 生成过程中请保持网络连接
echo   - 如遇问题请查看《使用手册.md》
echo.
echo ========================================
echo.
echo 按任意键关闭此窗口...
pause >nul
