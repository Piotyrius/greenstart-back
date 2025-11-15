#!/bin/bash
# GREWECO Backend - Local Development Startup Script (Linux/Mac)

echo "============================================"
echo "GREWECO Backend - Starting Local Server"
echo "============================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from env.example..."
    cp env.example .env
    echo ""
    echo "Please edit .env file with your settings"
    echo ""
    read -p "Press enter to continue..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check database
echo ""
echo "Checking database connection..."
python manage.py check --database default

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate

# Create superuser if needed
echo ""
echo "Checking for superuser..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Superuser exists:', User.objects.filter(is_superuser=True).exists())"

# Start development server
echo ""
echo "============================================"
echo "Starting Django development server..."
echo "Backend will be available at: http://localhost:8000"
echo "API will be available at: http://localhost:8000/api/"
echo "Admin panel at: http://localhost:8000/admin/"
echo "============================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver

