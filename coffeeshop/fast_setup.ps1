Write-Host "============================================" -ForegroundColor Green
Write-Host " Django Coffee Shop - Fast Setup Script" -ForegroundColor Green  
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Set-Location "c:\Users\aayus\Projects\CoffeeShop\coffeeshop"

Write-Host "[1/4] Running migrations..." -ForegroundColor Cyan
try {
    python manage.py migrate
    Write-Host "✓ Migrations completed" -ForegroundColor Green
} catch {
    Write-Host "✗ Migration failed: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

Write-Host "[2/4] Populating menu with new data..." -ForegroundColor Cyan
try {
    python manage.py populate_menu
    Write-Host "✓ Menu populated with 61+ items" -ForegroundColor Green
} catch {
    Write-Host "✗ Menu population failed: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

Write-Host "[3/4] Collecting static files..." -ForegroundColor Cyan
try {
    python manage.py collectstatic --noinput
    Write-Host "✓ Static files collected" -ForegroundColor Green
} catch {
    Write-Host "⚠ Static files warning (continuing...)" -ForegroundColor Yellow
}

Write-Host "[4/4] Starting Django server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "================================================" -ForegroundColor Yellow
Write-Host "   🚀 Coffee Shop Server Starting..." -ForegroundColor Yellow
Write-Host "   📱 Main Site: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "   📋 Menu Page: http://127.0.0.1:8000/menu/" -ForegroundColor White
Write-Host "   🔌 API Menu:  http://127.0.0.1:8000/api/menu/" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

python manage.py runserver 127.0.0.1:8000