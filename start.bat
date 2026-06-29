@echo off
chcp 65001 >nul
title EnterpriseQA System

set PROJECT_ROOT=%~dp0

echo [1/3] Starting Flask backend (port 5000)...
start /min "" "%PROJECT_ROOT%server\venv\Scripts\python.exe" "%PROJECT_ROOT%server\app.py"
echo       Backend started

echo [2/3] Starting Vue3 frontend (port 5173)...
start /min "" cmd /c "cd /d "%PROJECT_ROOT%client" && npm run dev"
echo       Frontend started

echo [3/3] Waiting for services...
ping 127.0.0.1 -n 5 >nul

echo.
echo ========================================
echo  EnterpriseQA System - Started!
echo ========================================
echo.
echo  Frontend: http://localhost:5173
echo  Backend:  http://localhost:5000
echo.
echo  Login: admin / 123456
echo.
pause >nul
start http://localhost:5173
pause >nul
