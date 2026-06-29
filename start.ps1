# ============================================
# 企业知识库问答系统 - 一键启动脚本 (PowerShell)
# 同时启动后端 Flask 和前端 Vite 开发服务器
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  企业知识库问答系统 - 正在启动..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 获取脚本所在目录（项目根目录）
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# 启动后端 Flask 服务
Write-Host "[1/3] 启动后端 Flask 服务 (端口 5000)..." -ForegroundColor Yellow
$serverDir = Join-Path $ProjectRoot "server"
$pythonExe = Join-Path $serverDir "venv/Scripts/python.exe"
$appPy = Join-Path $serverDir "app.py"

# 在独立窗口中启动后端（隐藏窗口）
$backendJob = Start-Process -WindowStyle Hidden -FilePath $pythonExe -ArgumentList $appPy -WorkingDirectory $serverDir -PassThru
Write-Host "      后端进程 PID: $($backendJob.Id)" -ForegroundColor Green

# 启动前端 Vite 开发服务
Write-Host "[2/3] 启动前端 Vue3 开发服务 (端口 5173)..." -ForegroundColor Yellow
$clientDir = Join-Path $ProjectRoot "client"

# 在独立窗口中启动前端
$frontendJob = Start-Process -WindowStyle Hidden -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory $clientDir -PassThru
Write-Host "      前端进程 PID: $($frontendJob.Id)" -ForegroundColor Green

# 等待服务启动
Write-Host "[3/3] 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 4

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  前端地址： http://localhost:5173" -ForegroundColor White
Write-Host "  后端地址： http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "  测试账号：admin / 123456" -ForegroundColor White
Write-Host ""

# 自动打开浏览器
Start-Process "http://localhost:5173"

# 提示如何关闭
Write-Host "  按任意键停止所有服务..." -ForegroundColor Magenta
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# 停止服务
Write-Host "正在停止服务..." -ForegroundColor Yellow
Stop-Process -Id $backendJob.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $frontendJob.Id -Force -ErrorAction SilentlyContinue
Write-Host "服务已停止" -ForegroundColor Green
