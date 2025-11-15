# GREWECO Backend - Project Structure

## Directory Structure

```
greweco-back/                    # Repository root (can have hyphens)
├── manage.py                    # Django management script
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Google Cloud Run deployment
├── cloudbuild.yaml             # CI/CD pipeline
├── docker-compose.yml          # Local development
├── .gcloudignore              # Files excluded from Cloud deployment
├── env.example                 # Environment variables template
│
├── greweco_back/              # Django project folder (MUST use underscore for Python)
│   ├── __init__.py
│   ├── settings.py            # Django settings (Google Cloud ready)
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI for Cloud Run
│   └── asgi.py                # ASGI (for future async)
│
└── apps/                       # Django applications
    ├── core/                  # Main business logic
    │   ├── models.py         # B2B/B2C models, Plantations, Purchases, NFTs
    │   ├── serializers.py    # API serializers
    │   ├── views.py          # API viewsets
    │   ├── urls.py           # API routes
    │   ├── admin.py          # Admin panel
    │   ├── migrations/       # Database migrations
    │   ├── tests/            # Unit and API tests
    │   ├── utils/            # Utilities
    │   │   ├── co2_calculator.py
    │   │   ├── pdf_generator.py
    │   │   └── logo_uploader.py
    │   └── management/       # Management commands
    │       └── commands/
    │           ├── update_ndvi_data.py
    │           └── update_co2_absorption.py
    │
    └── authentication/       # JWT authentication
        ├── views.py
        └── urls.py
```

## Why This Structure?

### Repository Name: `greweco-back` (with hyphen)
- ✅ Standard for Git repositories
- ✅ Works with GitHub/GitLab
- ✅ Clear and readable

### Django Project: `greweco_back` (with underscore)
- ✅ **Required by Python** - module names cannot have hyphens
- ✅ Standard Django convention
- ✅ Referenced in `manage.py` and `settings.py`

### This is NOT confusing because:
1. **Repository** (`greweco-back`) = Git repo, can have hyphens
2. **Django project** (`greweco_back`) = Python module, must use underscore
3. They serve different purposes and are in different contexts

## Google Cloud Deployment

### Files for Cloud Run:
- ✅ `Dockerfile` - Builds container image
- ✅ `cloudbuild.yaml` - CI/CD pipeline
- ✅ `.gcloudignore` - Excludes unnecessary files
- ✅ `requirements.txt` - Python dependencies
- ✅ `greweco_back/wsgi.py` - WSGI application entry point

### Environment Variables:
All configured in `env.example` and `settings.py`:
- Database (Cloud SQL)
- Google Cloud Storage
- JWT secrets
- CORS origins

## Verification

All references are correct:
- ✅ `manage.py` → `greweco_back.settings`
- ✅ `Dockerfile` → `greweco_back.wsgi:application`
- ✅ `wsgi.py` → `greweco_back.wsgi`
- ✅ `settings.py` → `BASE_DIR` correctly set

## Status

🟢 **Structure is correct and Google Cloud ready!**

No changes needed - this follows Django and Python best practices.

