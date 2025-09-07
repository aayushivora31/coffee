# Django Coffee Shop Startup Script
Write-Host "Starting Django Coffee Shop..." -ForegroundColor Green

# Navigate to project directory
Set-Location "c:\Users\aayus\Projects\CoffeeShop\coffeeshop"

# Check if manage.py exists
if (-not (Test-Path "manage.py")) {
    Write-Host "Error: manage.py not found in current directory!" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    exit 1
}

# Run migrations
Write-Host "Creating migrations..." -ForegroundColor Yellow
python manage.py makemigrations

Write-Host "Applying migrations..." -ForegroundColor Yellow
python manage.py migrate

# Create superuser if needed
Write-Host "Setting up superuser..." -ForegroundColor Yellow
python manage.py setup_superuser

# Populate menu data
Write-Host "Populating menu data..." -ForegroundColor Yellow
python manage.py populate_menu

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Start the development server
Write-Host "Starting Django development server..." -ForegroundColor Green
Write-Host "Your site will be available at: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Admin Dashboard: http://127.0.0.1:8000/dashboard/" -ForegroundColor Cyan
Write-Host "Django Admin: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Admin Credentials:" -ForegroundColor Yellow
Write-Host "Username: aayushi2001" -ForegroundColor White
Write-Host "Email: aayushivora31@gmail.com" -ForegroundColor White
Write-Host "Password: Aayu$2001" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red

python manage.py runserver