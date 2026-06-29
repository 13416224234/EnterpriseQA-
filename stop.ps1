# ============================================
# 停止所有服务
# ============================================
Write-Host "正在停止所有服务..." -ForegroundColor Yellow

# 停止 Python 进程（Flask）
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -match "app.py"
} | Stop-Process -Force -ErrorAction SilentlyContinue

# 停止 Node 进程（Vite）
Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -match "vite"
} | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "所有服务已停止" -ForegroundColor Green
