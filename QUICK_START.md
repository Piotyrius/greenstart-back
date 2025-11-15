# Quick Start Guide - GREWECO Backend

Get the backend running in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- PostgreSQL installed and running
- (Optional) Virtual environment

## Step 1: Install Dependencies

### Option A: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Install Globally

```bash
pip install -r requirements.txt
```

## Step 2: Configure Environment

```bash
# Copy environment template
copy env.example .env
# On Linux/Mac: cp env.example .env

# Edit .env file with your settings:
# - Database credentials
# - Secret keys
# - Google Cloud settings (optional for local dev)
```

Minimum `.env` configuration for local development:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=greweco_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
USE_CLOUD_SQL=False
```

## Step 3: Set Up Database

```bash
# Create PostgreSQL database (if not exists)
createdb greweco_db
# Or using psql:
# psql -U postgres
# CREATE DATABASE greweco_db;
```

## Step 4: Run Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

## Step 6: Run Development Server

```bash
python manage.py runserver
```

The API will be available at:
- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

## Step 7: Test the Setup

### Test API Endpoints

```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}'
```

### Run Tests

```bash
python manage.py test
```

## Troubleshooting

### Django Not Found
- Make sure virtual environment is activated
- Verify: `pip list | grep Django`
- Reinstall: `pip install -r requirements.txt`

### Database Connection Error
- Check PostgreSQL is running: `pg_isready`
- Verify database exists: `psql -l | grep greweco_db`
- Check `.env` file has correct DATABASE_* settings

### Migration Errors
- Delete migration files in `apps/*/migrations/` (except `__init__.py`)
- Run: `python manage.py makemigrations` again
- Then: `python manage.py migrate`

### Port Already in Use
- Change port: `python manage.py runserver 8001`
- Or kill process using port 8000

## Next Steps

1. **Create Test Data**: Use Django admin or API to create:
   - Developer
   - Building
   - Apartment
   - Plantation
   - Certificate

2. **Test CO₂ Calculations**: 
   ```bash
   python manage.py shell
   >>> from apps.core.models import Plantation
   >>> p = Plantation.objects.first()
   >>> p.calculate_yearly_co2()
   ```

3. **Generate PDF Certificate**:
   - Create a certificate via API
   - Call: `POST /api/certificates/{id}/generate_pdf/`

4. **Run Background Jobs**:
   ```bash
   python manage.py update_ndvi_data
   python manage.py update_co2_absorption
   ```

## Production Deployment

See `GOOGLE_CLOUD_SETUP.md` for deploying to Google Cloud Run.

