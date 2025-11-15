# Start GREWECO Backend Server
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Starting GREWECO Backend Server" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "Warning: .env file not found. Creating default..." -ForegroundColor Yellow
    "SECRET_KEY=django-insecure-local-dev-key-change-in-production-please`nDEBUG=True`nALLOWED_HOSTS=localhost,127.0.0.1`nDATABASE_HOST=`nUSE_CLOUD_SQL=False`nCORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000`nPORT=8000" | Out-File -FilePath .env -Encoding ASCII
}

# Check if virtual environment exists
if (Test-Path venv) {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    .\venv\Scripts\Activate.ps1
}

# Run migrations
Write-Host "Running migrations..." -ForegroundColor Cyan
python manage.py migrate --noinput

Write-Host ""
Write-Host "Starting Django development server on http://localhost:8000" -ForegroundColor Green
Write-Host "API will be available at: http://localhost:8000/api/" -ForegroundColor Green
Write-Host "Admin panel: http://localhost:8000/admin/" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start server
python manage.py runserver

