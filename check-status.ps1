Write-Host "==> 检查服务状态..." -ForegroundColor Cyan
Write-Host ""

# 检查后端 API
Write-Host "后端 API (端口 8000):" -ForegroundColor Yellow
$backend = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($backend) {
    Write-Host "  ✓ 运行中 (PID: $($backend.OwningProcess))" -ForegroundColor Green
    Write-Host "  访问: http://localhost:8000/docs" -ForegroundColor Gray
} else {
    Write-Host "  ✗ 未运行" -ForegroundColor Red
}

Write-Host ""

# 检查管理后台
Write-Host "管理后台 (端口 5173):" -ForegroundColor Yellow
$admin = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if ($admin) {
    Write-Host "  ✓ 运行中 (PID: $($admin.OwningProcess))" -ForegroundColor Green
    Write-Host "  访问: http://localhost:5173" -ForegroundColor Gray
} else {
    Write-Host "  ✗ 未运行" -ForegroundColor Red
}

Write-Host ""

# 检查 MySQL
Write-Host "MySQL (端口 3306):" -ForegroundColor Yellow
$mysql = docker-compose ps mysql 2>$null | Select-String "Up"
if ($mysql) {
    Write-Host "  ✓ 运行中" -ForegroundColor Green
} else {
    Write-Host "  ✗ 未运行" -ForegroundColor Red
}

Write-Host ""

# 检查 Redis
Write-Host "Redis (端口 6379):" -ForegroundColor Yellow
$redis = docker-compose ps redis 2>$null | Select-String "Up"
if ($redis) {
    Write-Host "  ✓ 运行中" -ForegroundColor Green
} else {
    Write-Host "  ✗ 未运行" -ForegroundColor Red
}

Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
