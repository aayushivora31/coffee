Write-Host "Starting Django Coffee Shop Server..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

Set-Location "c:\Users\aayus\Projects\CoffeeShop\coffeeshop"

Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

Write-Host "Checking if manage.py exists..." -ForegroundColor Cyan
if (Test-Path "manage.py") {
    Write-Host "✓ manage.py found" -ForegroundColor Green
} else {
    Write-Host "✗ manage.py not found - Please check directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

Write-Host ""
Write-Host "Running database migrations..." -ForegroundColor Cyan
python manage.py migrate

Write-Host ""
Write-Host "Starting Django development server..." -ForegroundColor Cyan
Write-Host "Open your browser and go to: http://127.0.0.1:8000/" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver 127.0.0.1:8000