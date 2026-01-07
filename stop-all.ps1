Write-Host "==> 停止所有服务..." -ForegroundColor Yellow

# 停止后端 API (端口 8000)
Write-Host "停止后端 API..." -ForegroundColor Gray
$backend = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($backend) {
    $pid = $backend.OwningProcess
    Stop-Process -Id $pid -Force
    Write-Host "  ✓ 后端 API 已停止" -ForegroundColor Green
} else {
    Write-Host "  - 后端 API 未运行" -ForegroundColor Gray
}

# 停止管理后台 (端口 5173)
Write-Host "停止管理后台..." -ForegroundColor Gray
$admin = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if ($admin) {
    $pid = $admin.OwningProcess
    Stop-Process -Id $pid -Force
    Write-Host "  ✓ 管理后台已停止" -ForegroundColor Green
} else {
    Write-Host "  - 管理后台未运行" -ForegroundColor Gray
}

# 停止 Docker 服务
Write-Host "停止 MySQL 和 Redis..." -ForegroundColor Gray
docker-compose stop mysql redis
Write-Host "  ✓ MySQL 和 Redis 已停止" -ForegroundColor Green

Write-Host ""
Write-Host "✅ 所有服务已停止!" -ForegroundColor Green
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
