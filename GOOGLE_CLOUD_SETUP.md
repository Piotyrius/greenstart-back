# Google Cloud Setup Guide

This guide helps you deploy the GREWECO backend to Google Cloud Platform using your Google for Startups credits.

## Prerequisites

- Google Cloud Project with billing enabled
- Google for Startups Cloud Program credits activated
- `gcloud` CLI installed and configured

## Step 1: Create Google Cloud Resources

### 1.1 Create Cloud SQL Instance

```bash
gcloud sql instances create greweco-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=YOUR_DB_PASSWORD
```

Get the connection name:
```bash
gcloud sql instances describe greweco-db --format="value(connectionName)"
# Output: project-id:us-central1:greweco-db
```

### 1.2 Create Database

```bash
gcloud sql databases create greweco_db --instance=greweco-db
```

### 1.3 Create Cloud Storage Bucket

```bash
gsutil mb -p YOUR_PROJECT_ID -l us-central1 gs://greweco-certificates
gsutil iam ch allUsers:objectViewer gs://greweco-certificates
```

### 1.4 Enable Required APIs

```bash
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  sqladmin.googleapis.com \
  storage-component.googleapis.com \
  cloudscheduler.googleapis.com
```

## Step 2: Configure Environment Variables

### 2.1 Local Development (.env file)

Copy `env.example` to `.env` and fill in:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-cloud-run-url.run.app
USE_CLOUD_SQL=True
CLOUD_SQL_CONNECTION_NAME=your-project:us-central1:greweco-db
DATABASE_NAME=greweco_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-db-password
GS_BUCKET_NAME=greweco-certificates
GOOGLE_CLOUD_PROJECT_ID=your-project-id
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CLOUD_SCHEDULER_SECRET=your-secret-token
```

### 2.2 Cloud Run Environment Variables

Set these in Cloud Run after deployment, or use:

```bash
gcloud run services update greweco-back \
  --set-env-vars="SECRET_KEY=your-secret,USE_CLOUD_SQL=True,CLOUD_SQL_CONNECTION_NAME=project:region:instance" \
  --region=us-central1
```

## Step 3: Deploy to Cloud Run

### 3.1 Build and Deploy

```bash
# Build and push image
gcloud builds submit --config cloudbuild.yaml

# Or deploy directly from source
gcloud run deploy greweco-back \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --add-cloudsql-instances=YOUR_PROJECT_ID:us-central1:greweco-db \
  --set-env-vars="USE_CLOUD_SQL=True,CLOUD_SQL_CONNECTION_NAME=YOUR_PROJECT_ID:us-central1:greweco-db,DATABASE_NAME=greweco_db,DATABASE_USER=postgres,DATABASE_PASSWORD=YOUR_PASSWORD,GS_BUCKET_NAME=greweco-certificates,GOOGLE_CLOUD_PROJECT_ID=YOUR_PROJECT_ID"
```

### 3.2 Grant Permissions

Grant Cloud Run service account access to Cloud SQL:

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

Grant access to Cloud Storage:

```bash
gsutil iam ch serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com:objectAdmin gs://greweco-certificates
```

## Step 4: Run Migrations

### 4.1 Connect to Cloud Run and Run Migrations

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe greweco-back --region=us-central1 --format="value(status.url)")

# Run migrations via Cloud Run
gcloud run services update greweco-back \
  --update-env-vars="RUN_MIGRATIONS=True" \
  --region=us-central1

# Or use Cloud SQL Proxy for local migration
cloud-sql-proxy YOUR_PROJECT_ID:us-central1:greweco-db
# Then run: python manage.py migrate
```

## Step 5: Set Up Cloud Scheduler

### 5.1 Create Scheduled Job for NDVI Updates

```bash
gcloud scheduler jobs create http update-ndvi-data \
  --schedule="0 0 1 1 *" \
  --uri="https://your-cloud-run-url.run.app/api/update-ndvi/" \
  --http-method=POST \
  --headers="X-CloudScheduler-Secret=YOUR_SECRET_TOKEN" \
  --oidc-service-account-email=YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --location=us-central1
```

### 5.2 Create Scheduled Job for CO₂ Updates

```bash
gcloud scheduler jobs create http update-co2-data \
  --schedule="0 0 1 * *" \
  --uri="https://your-cloud-run-url.run.app/api/update-co2/" \
  --http-method=POST \
  --headers="X-CloudScheduler-Secret=YOUR_SECRET_TOKEN" \
  --oidc-service-account-email=YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --location=us-central1
```

## Step 6: Verify Deployment

### 6.1 Test API Endpoints

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe greweco-back --region=us-central1 --format="value(status.url)")

# Test health (if you add a health endpoint)
curl $SERVICE_URL/api/

# Test authentication
curl -X POST $SERVICE_URL/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'
```

## Cost Optimization

With Google for Startups credits ($2,000 over 2 years):

- **Cloud Run**: Free tier includes 2 million requests/month
- **Cloud SQL**: db-f1-micro is ~$7/month (covered by credits)
- **Cloud Storage**: First 5GB free, then ~$0.020/GB/month
- **Cloud Scheduler**: 3 free jobs, then $0.10/job/month
- **Cloud Build**: 120 build-minutes/day free

## Monitoring

### View Logs

```bash
gcloud run services logs read greweco-back --region=us-central1
```

### Monitor Costs

```bash
# View current usage
gcloud billing accounts list
gcloud billing projects describe YOUR_PROJECT_ID
```

## Troubleshooting

### Cloud SQL Connection Issues

1. Verify connection name format: `project:region:instance`
2. Check Cloud Run has Cloud SQL connection added
3. Verify service account has `cloudsql.client` role

### Storage Issues

1. Verify bucket exists: `gsutil ls gs://greweco-certificates`
2. Check bucket permissions: `gsutil iam get gs://greweco-certificates`
3. Ensure service account has `storage.objectAdmin` role

### Environment Variables

All variables from `env.example` should be set in Cloud Run:
- Use `gcloud run services update` to set variables
- Or set in Cloud Console → Cloud Run → Service → Edit & Deploy New Revision → Variables & Secrets

## Next Steps

1. Set up CI/CD pipeline (Cloud Build)
2. Configure custom domain
3. Set up monitoring and alerts
4. Configure backup strategy for Cloud SQL
5. Set up Cloud CDN for static files (optional)

