#!/bin/bash
# Quick Django Coffee Shop Startup Script

echo "🚀 Starting Django Coffee Shop Server..."
echo "📍 Project: CoffeeShop Django Application"
echo "🌐 URL: http://127.0.0.1:8000/"
echo ""

# Navigate to project directory
cd coffeeshop

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Make sure you're in the correct directory."
    exit 1
fi

# Start the Django development server
echo "🔧 Starting Django development server..."
python manage.py runserver

echo ""
echo "✅ Server is running at http://127.0.0.1:8000/"
echo "📄 Menu page: http://127.0.0.1:8000/menu/"
echo ""
echo "Press Ctrl+C to stop the server"