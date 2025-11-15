# Google Cloud Deployment Guide - GREWECO Backend

## Project Structure for Cloud Run

The project structure is **optimized for Google Cloud Run deployment**:

```
greweco-back/                    # Repository root
├── manage.py                    # Django CLI
├── requirements.txt            # Dependencies
├── Dockerfile                  # Cloud Run container
├── cloudbuild.yaml             # CI/CD pipeline
├── .gcloudignore              # Exclude files from Cloud
│
├── greweco_back/              # Django project (Python module)
│   ├── settings.py            # Cloud SQL + GCS configured
│   ├── wsgi.py                # Cloud Run entry point
│   └── urls.py
│
└── apps/                       # Django apps
    ├── core/                  # Main business logic
    └── authentication/        # JWT auth
```

## Quick Deploy to Cloud Run

### 1. Set Up Google Cloud Resources

```bash
# Create Cloud SQL instance
gcloud sql instances create greweco-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create greweco_db --instance=greweco-db

# Create Cloud Storage bucket
gsutil mb -p YOUR_PROJECT_ID -l us-central1 gs://greweco-certificates
gsutil iam ch allUsers:objectViewer gs://greweco-certificates
```

### 2. Deploy to Cloud Run

```bash
# Option A: Direct deploy from source
gcloud run deploy greweco-back \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --add-cloudsql-instances=YOUR_PROJECT_ID:us-central1:greweco-db \
  --set-env-vars="USE_CLOUD_SQL=True,CLOUD_SQL_CONNECTION_NAME=YOUR_PROJECT_ID:us-central1:greweco-db,DATABASE_NAME=greweco_db,DATABASE_USER=postgres,DATABASE_PASSWORD=YOUR_PASSWORD,GS_BUCKET_NAME=greweco-certificates,GOOGLE_CLOUD_PROJECT_ID=YOUR_PROJECT_ID,SECRET_KEY=YOUR_SECRET_KEY,DEBUG=False"

# Option B: Build and deploy with Cloud Build
gcloud builds submit --config cloudbuild.yaml
```

### 3. Run Migrations

```bash
# Connect to Cloud Run and run migrations
gcloud run services update greweco-back \
  --update-env-vars="RUN_MIGRATIONS=True" \
  --region us-central1

# Or use Cloud SQL Proxy locally
cloud-sql-proxy YOUR_PROJECT_ID:us-central1:greweco-db
python manage.py migrate
```

## Environment Variables for Cloud Run

Set these in Cloud Run console or via CLI:

```env
# Django
SECRET_KEY=your-production-secret-key-50-chars-min
DEBUG=False
ALLOWED_HOSTS=greweco-back-xxxxx.run.app,your-domain.com

# Database (Cloud SQL)
USE_CLOUD_SQL=True
CLOUD_SQL_CONNECTION_NAME=project-id:us-central1:greweco-db
DATABASE_NAME=greweco_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-db-password

# Google Cloud Storage
GS_BUCKET_NAME=greweco-certificates
GOOGLE_CLOUD_PROJECT_ID=your-project-id
# GOOGLE_APPLICATION_CREDENTIALS= (leave empty - uses default service account)

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

# Cloud Scheduler
CLOUD_SCHEDULER_SECRET=your-secret-token

# Port (auto-set by Cloud Run)
PORT=8080
```

## Dockerfile Optimization

The Dockerfile is optimized for Cloud Run:
- ✅ Uses Python 3.11-slim (smaller image)
- ✅ Installs only necessary system packages
- ✅ Collects static files
- ✅ Uses PORT environment variable (Cloud Run requirement)
- ✅ Gunicorn configured for Cloud Run

## Cloud Build Pipeline

`cloudbuild.yaml` automates:
1. Build Docker image
2. Push to Container Registry
3. Deploy to Cloud Run

## Files Excluded from Cloud (.gcloudignore)

- Development files
- Documentation (kept in repo, not deployed)
- Local environment files
- Cache files

## Verification Checklist

Before deploying, verify:
- ✅ `Dockerfile` references `greweco_back.wsgi:application`
- ✅ `manage.py` references `greweco_back.settings`
- ✅ All environment variables in `env.example`
- ✅ Cloud SQL connection string format correct
- ✅ Cloud Storage bucket exists
- ✅ Service account has required permissions

## Post-Deployment

1. **Run migrations**: `gcloud run services exec greweco-back -- python manage.py migrate`
2. **Create superuser**: `gcloud run services exec greweco-back -- python manage.py createsuperuser`
3. **Test API**: `curl https://greweco-back-xxxxx.run.app/api/`
4. **Set up Cloud Scheduler**: For NDVI/CO₂ updates

## Cost Optimization

With Google for Startups credits:
- **Cloud Run**: Free tier (2M requests/month)
- **Cloud SQL**: db-f1-micro ~$7/month (covered by credits)
- **Cloud Storage**: 5GB free, then $0.020/GB/month
- **Cloud Build**: 120 build-minutes/day free

## Status

🟢 **Project structure is clean and Google Cloud optimized!**

All files correctly reference `greweco_back` (Django project) while repository is `greweco-back`.

