#!/usr/bin/env python
"""
Backend Setup Script
Helps set up the GREWECO backend for first-time use.
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Step: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def check_file_exists(filepath, description):
    """Check if a required file exists."""
    if os.path.exists(filepath):
        print(f"✓ {description} exists")
        return True
    else:
        print(f"✗ {description} missing: {filepath}")
        return False

def main():
    print("="*60)
    print("GREWECO Backend Setup")
    print("="*60)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 11):
        print("⚠ Warning: Python 3.11+ recommended")
    else:
        print(f"✓ Python {python_version.major}.{python_version.minor} detected")
    
    # Check required files
    print("\nChecking required files...")
    required_files = [
        ("manage.py", "Django management script"),
        ("requirements.txt", "Python dependencies"),
        ("greweco_back/settings.py", "Django settings"),
        ("apps/core/models.py", "Core models"),
        ("apps/core/views.py", "API views"),
        ("apps/authentication/views.py", "Authentication views"),
    ]
    
    all_files_exist = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    if not all_files_exist:
        print("\n❌ Some required files are missing. Please check the project structure.")
        return
    
    print("\n✓ All required files found")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("\n⚠ .env file not found. Creating from env.example...")
        if os.path.exists('env.example'):
            with open('env.example', 'r') as src:
                with open('.env', 'w') as dst:
                    dst.write(src.read())
            print("✓ Created .env file from env.example")
            print("⚠ Please edit .env with your actual configuration values")
        else:
            print("⚠ env.example not found. Please create .env manually")
    
    # Install dependencies
    print("\n" + "="*60)
    response = input("Install Python dependencies? (y/n): ")
    if response.lower() == 'y':
        if not run_command("pip install -r requirements.txt", "Installing dependencies"):
            print("❌ Failed to install dependencies")
            return
        print("✓ Dependencies installed")
    
    # Create migrations
    print("\n" + "="*60)
    response = input("Create database migrations? (y/n): ")
    if response.lower() == 'y':
        if not run_command("python manage.py makemigrations", "Creating migrations"):
            print("❌ Failed to create migrations")
            return
        print("✓ Migrations created")
    
    # Run migrations
    print("\n" + "="*60)
    response = input("Run database migrations? (y/n): ")
    if response.lower() == 'y':
        if not run_command("python manage.py migrate", "Running migrations"):
            print("❌ Failed to run migrations")
            print("⚠ Make sure PostgreSQL is running and DATABASE_* settings in .env are correct")
            return
        print("✓ Migrations applied")
    
    # Create superuser
    print("\n" + "="*60)
    response = input("Create Django superuser? (y/n): ")
    if response.lower() == 'y':
        print("Please enter superuser details:")
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    # Collect static files
    print("\n" + "="*60)
    response = input("Collect static files? (y/n): ")
    if response.lower() == 'y':
        run_command("python manage.py collectstatic --noinput", "Collecting static files")
        print("✓ Static files collected")
    
    # Run tests
    print("\n" + "="*60)
    response = input("Run tests? (y/n): ")
    if response.lower() == 'y':
        if run_command("python manage.py test", "Running tests"):
            print("✓ All tests passed")
        else:
            print("⚠ Some tests failed. Check the output above.")
    
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit .env file with your database and Google Cloud settings")
    print("2. Run: python manage.py runserver")
    print("3. Access admin at: http://localhost:8000/admin/")
    print("4. API available at: http://localhost:8000/api/")
    print("\nFor production deployment, see GOOGLE_CLOUD_SETUP.md")

if __name__ == "__main__":
    main()

