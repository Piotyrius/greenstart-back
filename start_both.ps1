# Start Both Backend and Frontend Servers
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Starting GREWECO - Backend + Frontend" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Start backend in new window
Write-Host "Starting backend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-File", "D:\greweco-back\start_backend.ps1"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend in new window
Write-Host "Starting frontend server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-File", "D:\greweco-front\start_frontend.ps1"

Write-Host ""
Write-Host "✅ Both servers are starting in separate windows!" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Close the windows or press Ctrl+C to stop the servers" -ForegroundColor Cyan

