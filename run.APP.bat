@echo off
chcp 65001
title 肝癌症药物分析平台

echo.
echo ===============================================
echo       肝癌症药物分析平台
echo ===============================================
echo.

echo 1. 正在设置环境变量...
set PATH=C:\Users\Administrator\anaconda3;C:\Users\Administrator\anaconda3\Scripts;C:\Users\Administrator\anaconda3\Library\bin;%PATH%

echo 2. 检查Python环境...
python --version
if errorlevel 1 (
    echo [错误] Python不可用
    pause
    exit /b 1
)

echo 3. 启动Streamlit服务器...
echo    应用将在 http://localhost:8501 运行
echo.

REM 启动Streamlit（不等待它完成）
start "Streamlit Server" cmd /k "python -m streamlit run app.py --server.port 8501 --server.address localhost"

echo 4. 等待服务器启动...
timeout /t 5 /nobreak >nul

echo 5. 打开浏览器...
start "" "http://localhost:8501"

echo.
echo ✅ 启动完成！
echo 📊 应用地址: http://localhost:8501
echo ⚠️  请勿关闭Streamlit服务器窗口（黑色窗口）
echo.
echo 按任意键关闭此启动窗口...
pause >nul