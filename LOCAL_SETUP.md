# Local Development Setup Guide

## Quick Start (Easiest - SQLite)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd D:\greweco-back
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **The .env file is already created** - it's configured for local development

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start server:**
   ```bash
   python manage.py runserver
   ```

   Backend will be available at: **http://localhost:8000**

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd D:\greweco-front
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **The .env.local file is already created** - it points to `http://localhost:8000`

4. **Start development server:**
   ```bash
   npm run dev
   ```

   Frontend will be available at: **http://localhost:3000**

---

## Using Startup Scripts (Easiest)

### Windows:

**Backend:**
```bash
cd D:\greweco-back
run_local.bat
```

**Frontend (in new terminal):**
```bash
cd D:\greweco-front
run_local.bat
```

### Linux/Mac:

**Backend:**
```bash
cd D:\greweco-back
chmod +x run_local.sh
./run_local.sh
```

**Frontend (in new terminal):**
```bash
cd D:\greweco-front
chmod +x run_local.sh
./run_local.sh
```

---

## Using PostgreSQL (Docker)

If you prefer PostgreSQL instead of SQLite:

### 1. Start PostgreSQL with Docker:

```bash
cd D:\greweco-back
docker-compose up -d db
```

This starts PostgreSQL on `localhost:5432`

### 2. Update .env file:

The `.env` file is already configured for PostgreSQL. Just make sure:
- `USE_CLOUD_SQL=False`
- Database settings match docker-compose.yml

### 3. Run migrations:

```bash
python manage.py migrate
```

### 4. Start backend:

```bash
python manage.py runserver
```

---

## Access Points

Once both servers are running:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/
- **API Root:** http://localhost:8000/api/

---

## Troubleshooting

### Backend Issues:

1. **"Module not found" errors:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database connection errors:**
   - Check `.env` file settings
   - For PostgreSQL: Make sure docker-compose is running
   - For SQLite: No setup needed, it's automatic

3. **Port 8000 already in use:**
   ```bash
   python manage.py runserver 8001
   ```
   Then update frontend `.env.local` to `http://localhost:8001`

### Frontend Issues:

1. **"Cannot connect to API":**
   - Make sure backend is running on port 8000
   - Check `.env.local` has correct API URL

2. **"Module not found" errors:**
   ```bash
   npm install
   ```

3. **Port 3000 already in use:**
   ```bash
   PORT=3001 npm run dev
   ```

---

## Creating Test Data

### Create a superuser:
```bash
python manage.py createsuperuser
```

### Access admin panel:
- Go to: http://localhost:8000/admin/
- Login with superuser credentials

### Create test data via admin:
- Create Buyers (B2B/B2C)
- Create Plantations
- Create Tree Lots
- Create Purchases

---

## Next Steps

1. ✅ Backend running on http://localhost:8000
2. ✅ Frontend running on http://localhost:3000
3. ✅ Create superuser for admin access
4. ✅ Test API endpoints
5. ✅ Test frontend login/registration

---

## Development Tips

- **Backend changes:** Django auto-reloads on file changes
- **Frontend changes:** Next.js hot-reloads automatically
- **Database changes:** Run `python manage.py makemigrations` then `migrate`
- **API testing:** Use http://localhost:8000/api/ or Postman
- **View logs:** Check terminal output for both servers

