# GREWECO Backend

Django REST Framework backend for the GREWECO Green Web3 CO₂ Removal Platform.

## Overview

This backend provides a RESTful API for managing:
- Developers and construction projects
- Buildings and apartments
- Paulownia plantations and hectare lots
- CO₂ absorption certificates
- Growth data and analytics

## Features

- **CO₂ Absorption Calculations**: Automatic calculation of CO₂ absorption based on plantation age, species factors, and area
- **JWT Authentication**: Secure token-based authentication for developers and admins
- **PDF Certificate Generation**: Automated PDF certificate generation with QR codes
- **Google Cloud Storage Integration**: Upload certificates to GCS for public access
- **Background Jobs**: Management commands for updating NDVI and CO₂ data
- **Comprehensive API**: Full CRUD operations for all models

## Tech Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL (Cloud SQL ready)
- Google Cloud Storage
- JWT Authentication (djangorestframework-simplejwt)

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Google Cloud account (for Cloud Storage)

### Local Development

1. **Clone the repository**
   ```bash
   cd greweco-back
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_NAME=greweco_db
   DATABASE_USER=postgres
   DATABASE_PASSWORD=postgres
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   GS_BUCKET_NAME=greweco-certificates
   ```

5. **Set up PostgreSQL database**
   ```bash
   createdb greweco_db
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

### Using Docker Compose

1. **Start services**
   ```bash
   docker-compose up -d
   ```

2. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## API Documentation

### Authentication

#### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "developer1",
  "email": "dev@example.com",
  "password": "securepassword"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "developer1",
  "password": "securepassword"
}
```

Response:
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "developer1",
    "email": "dev@example.com"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

#### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "refresh_token_here"
}
```

### API Endpoints

All endpoints require authentication (JWT token in Authorization header):
```
Authorization: Bearer <access_token>
```

#### Developers
- `GET /api/developers/` - List all developers
- `GET /api/developers/{id}/` - Get developer details
- `POST /api/developers/` - Create developer (admin only)
- `PUT /api/developers/{id}/` - Update developer (admin only)
- `DELETE /api/developers/{id}/` - Delete developer (admin only)

#### Buildings
- `GET /api/buildings/` - List buildings (filter: `?developer={id}`)
- `GET /api/buildings/{id}/` - Get building details
- `POST /api/buildings/` - Create building (admin only)
- `PUT /api/buildings/{id}/` - Update building (admin only)
- `DELETE /api/buildings/{id}/` - Delete building (admin only)

#### Apartments
- `GET /api/apartments/` - List apartments (filter: `?building={id}`)
- `GET /api/apartments/{id}/` - Get apartment details
- `POST /api/apartments/` - Create apartment
- `PUT /api/apartments/{id}/` - Update apartment
- `DELETE /api/apartments/{id}/` - Delete apartment

#### Plantations
- `GET /api/plantations/` - List plantations (includes `yearly_co2_absorbed`)
- `GET /api/plantations/{id}/` - Get plantation details
- `GET /api/plantations/{id}/co2_calculation/` - Get detailed CO₂ calculation breakdown
- `POST /api/plantations/{id}/assign_hectare/{building_id}/` - Assign hectare to building
- `POST /api/plantations/` - Create plantation (admin only)
- `PUT /api/plantations/{id}/` - Update plantation (admin only)
- `DELETE /api/plantations/{id}/` - Delete plantation (admin only)

#### Certificates
- `GET /api/certificates/` - List certificates (filter: `?apartment={id}`)
- `GET /api/certificates/{id}/` - Get certificate details (includes `co2_absorbed_kg`)
- `POST /api/certificates/` - Create certificate
- `POST /api/certificates/{id}/generate_pdf/` - Generate and upload PDF certificate

#### Growth Data
- `GET /api/growth-data/` - List growth data (filter: `?plantation={id}`)
- `POST /api/growth-data/` - Create growth data record

## CO₂ Calculation

The system calculates CO₂ absorption using the following formula:

```
CO₂_per_year = age_years × species_factor × hectares × trees_per_hectare × scale_factor
```

Where:
- `age_years` = years since planting date
- `species_factor` = 22 kg CO₂ per tree per year (PLACEHOLDER)
- `trees_per_hectare` = 1000 (PLACEHOLDER)
- `scale_factor` = 1.0 (PLACEHOLDER)

**Note**: These values are placeholders and should be replaced with real biomass-based calculations in future iterations.

For apartment certificates, CO₂ is calculated as:
```
apartment_co2 = plantation_co2 × (hectare_lot_area / plantation_total_area) × (apartment_area / building_total_area)
```

## Management Commands

### Update NDVI and CO₂ Data
```bash
python manage.py update_ndvi_data
python manage.py update_ndvi_data --year 2024
```

### Recalculate CO₂ Absorption
```bash
python manage.py update_co2_absorption
python manage.py update_co2_absorption --certificate-id 1
```

## Testing

Run tests:
```bash
python manage.py test
```

Run specific test:
```bash
python manage.py test apps.core.tests.test_models
python manage.py test apps.core.tests.test_api
python manage.py test apps.core.tests.test_co2_calculator
```

## Google Cloud Deployment

### Prerequisites

- Google Cloud Project with billing enabled
- Cloud SQL instance (PostgreSQL)
- Cloud Storage bucket
- Cloud Run service account with appropriate permissions

### Environment Variables for Cloud Run

Set these in Cloud Run service configuration:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-cloud-run-url
USE_CLOUD_SQL=True
CLOUD_SQL_CONNECTION_NAME=project:region:instance
DATABASE_NAME=greweco_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-db-password
GS_BUCKET_NAME=greweco-certificates
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
CORS_ALLOWED_ORIGINS=https://your-frontend-url
```

### Deploy to Cloud Run

1. **Build and push Docker image**
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

2. **Or deploy directly**
   ```bash
   gcloud run deploy greweco-back \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

3. **Set environment variables**
   ```bash
   gcloud run services update greweco-back \
     --set-env-vars KEY=VALUE
   ```

### Cloud SQL Connection

For Cloud SQL, configure the connection string:
```env
CLOUD_SQL_CONNECTION_NAME=project:region:instance
USE_CLOUD_SQL=True
```

The application will automatically use Unix socket connection when `USE_CLOUD_SQL=True`.

### Cloud Scheduler Setup

Create a scheduled job to update CO₂ data yearly:

```bash
gcloud scheduler jobs create http update-co2-data \
  --schedule="0 0 1 1 *" \
  --uri="https://your-cloud-run-url/api/update-co2/" \
  --http-method=POST \
  --oidc-service-account-email=your-service-account@project.iam.gserviceaccount.com
```

## Project Structure

```
greweco-back/
├── apps/
│   ├── core/
│   │   ├── models.py          # Django models
│   │   ├── serializers.py     # DRF serializers
│   │   ├── views.py           # API views
│   │   ├── urls.py            # URL routing
│   │   ├── admin.py            # Admin panel
│   │   ├── utils/
│   │   │   ├── co2_calculator.py  # CO₂ calculation utilities
│   │   │   └── pdf_generator.py    # PDF generation
│   │   ├── management/
│   │   │   └── commands/      # Management commands
│   │   └── tests/              # Unit and API tests
│   └── authentication/
│       ├── views.py           # Auth endpoints
│       └── urls.py
├── greweco_back/
│   ├── settings.py            # Django settings
│   ├── urls.py                # Root URL config
│   └── wsgi.py
├── requirements.txt
├── Dockerfile
├── cloudbuild.yaml
└── docker-compose.yml
```

## Future Improvements

- Replace placeholder CO₂ calculation with real biomass-based formulas
- Integrate real NDVI data from satellite APIs
- Add Web3 NFT certificate minting
- MongoDB Atlas integration for analytics
- Timber revenue tracking
- ESG reporting module

## License

Proprietary - GREWECO Platform
