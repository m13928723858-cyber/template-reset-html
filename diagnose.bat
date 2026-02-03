@echo off
chcp 65001 >nul
echo ========================================
echo    Brand Swap 诊断工具
echo ========================================
echo.

echo [检查1] 后端虚拟环境
if exist "backend\.venv\Scripts\python.exe" (
    echo ✓ 后端虚拟环境存在
) else (
    echo ✗ 后端虚拟环境不存在
    echo   解决: cd backend ^&^& python -m venv .venv ^&^& .venv\Scripts\activate ^&^& pip install -r requirements.txt
)
echo.

echo [检查2] 前端依赖
if exist "frontend\node_modules" (
    echo ✓ 前端依赖已安装
) else (
    echo ✗ 前端依赖未安装
    echo   解决: cd frontend ^&^& npm install
)
echo.

echo [检查3] 后端环境变量
if exist "backend\.env" (
    echo ✓ 后端 .env 文件存在
    findstr /C:"DOLPHIN_API_KEY" backend\.env >nul
    if %errorlevel% equ 0 (
        echo ✓ DOLPHIN_API_KEY 已配置
    ) else (
        echo ✗ DOLPHIN_API_KEY 未配置
    )
) else (
    echo ✗ 后端 .env 文件不存在
)
echo.

echo [检查4] 后端服务状态
netstat -ano | findstr ":8000" >nul
if %errorlevel% equ 0 (
    echo ✓ 后端服务正在运行 (端口 8000)
) else (
    echo ✗ 后端服务未运行
    echo   解决: cd backend ^&^& .venv\Scripts\activate ^&^& python main.py
)
echo.

echo [检查5] 前端服务状态
netstat -ano | findstr ":5174" >nul
if %errorlevel% equ 0 (
    echo ✓ 前端服务正在运行 (端口 5174)
) else (
    echo ✗ 前端服务未运行
    echo   解决: cd frontend ^&^& npm run dev
)
echo.

echo [检查6] 必要目录
set all_dirs_exist=1
for %%d in (backend\uploads backend\outputs backend\temp) do (
    if exist "%%d" (
        echo ✓ %%d 存在
    ) else (
        echo ✗ %%d 不存在
        set all_dirs_exist=0
    )
)
echo.

echo ========================================
echo    诊断完成
echo ========================================
echo.
echo 如果所有检查都通过，请访问:
echo   新版: http://localhost:5174/?mode=simple
echo   旧版: http://localhost:5174/
echo.
pause
