# 启动所有服务
Write-Host "==> 启动 MySQL 和 Redis..." -ForegroundColor Green
docker-compose up -d mysql redis
Start-Sleep -Seconds 5

# 启动后端 API
Write-Host "==> 启动后端 API..." -ForegroundColor Green
Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd server; venv\Scripts\activate; python -m app.main"

Start-Sleep -Seconds 3

# 启动管理后台
Write-Host "==> 启动管理后台..." -ForegroundColor Green
Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd admin; npm run dev"

Write-Host ""
Write-Host "✅ 所有服务已启动!" -ForegroundColor Green
Write-Host ""
Write-Host "访问地址:" -ForegroundColor Cyan
Write-Host "  后端 API:  http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "  管理后台:  http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
