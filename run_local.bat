@echo off
REM GREWECO Backend - Local Development Startup Script (Windows)

echo ============================================
echo GREWECO Backend - Starting Local Server
echo ============================================
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env file for local development...
    (
        echo # GREWECO Backend - Local Development
        echo SECRET_KEY=django-insecure-local-dev-key-change-in-production-12345
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo USE_CLOUD_SQL=False
        echo DATABASE_HOST=
        echo CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
        echo PORT=8000
    ) > .env
    echo .env file created with default local settings
    echo.
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Check database
echo.
echo Checking database connection...
python manage.py check --database default

REM Run migrations
echo.
echo Running database migrations...
python manage.py migrate

REM Create superuser if needed
echo.
echo Checking for superuser...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Superuser exists:', User.objects.filter(is_superuser=True).exists())" 2>nul

REM Start development server
echo.
echo ============================================
echo Starting Django development server...
echo Backend will be available at: http://localhost:8000
echo API will be available at: http://localhost:8000/api/
echo Admin panel at: http://localhost:8000/admin/
echo ============================================
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

