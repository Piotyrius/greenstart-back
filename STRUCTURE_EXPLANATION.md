# Project Structure Explanation

## Why Two Similar Names?

### Repository: `greweco-back` (with hyphen)
- ✅ Git repository name (can use hyphens)
- ✅ Standard naming convention
- ✅ Clear and readable

### Django Project: `greweco_back` (with underscore)
- ✅ **Python requirement** - module names CANNOT have hyphens
- ✅ Standard Django convention
- ✅ Used in imports: `from greweco_back import settings`

## This is Standard Django Practice

```
greweco-back/              ← Repository (Git)
├── manage.py
├── requirements.txt
├── Dockerfile
└── greweco_back/          ← Django project (Python module)
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

**This is NOT confusing** - they serve different purposes:
- Repository = Git/GitHub folder
- Django project = Python package (must use underscore)

## All References Are Correct

✅ `manage.py` → `greweco_back.settings`
✅ `Dockerfile` → `greweco_back.wsgi:application`
✅ `wsgi.py` → `greweco_back.wsgi`
✅ `settings.py` → `ROOT_URLCONF = 'greweco_back.urls'`

## Google Cloud Ready

✅ Dockerfile correctly references `greweco_back.wsgi`
✅ Cloud Build config uses repository name `greweco-back`
✅ All environment variables configured
✅ Cloud SQL connection ready
✅ Cloud Storage integration ready

## Status

🟢 **Structure is correct and optimized for Google Cloud!**

No changes needed - this follows Django and Python best practices.

