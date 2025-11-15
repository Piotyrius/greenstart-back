# 🚀 Quick Start - Run GREWECO Locally

## Option 1: Use Startup Scripts (Easiest!)

### Windows:

**Terminal 1 - Backend:**
```bash
cd D:\greweco-back
run_local.bat
```

**Terminal 2 - Frontend:**
```bash
cd D:\greweco-front
run_local.bat
```

### Linux/Mac:

**Terminal 1 - Backend:**
```bash
cd D:\greweco-back
chmod +x run_local.sh
./run_local.sh
```

**Terminal 2 - Frontend:**
```bash
cd D:\greweco-front
chmod +x run_local.sh
./run_local.sh
```

---

## Option 2: Manual Setup

### Backend Setup:

1. **Navigate to backend:**
   ```bash
   cd D:\greweco-back
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start server:**
   ```bash
   python manage.py runserver
   ```

   ✅ Backend: http://localhost:8000

### Frontend Setup:

1. **Navigate to frontend:**
   ```bash
   cd D:\greweco-front
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start server:**
   ```bash
   npm run dev
   ```

   ✅ Frontend: http://localhost:3000

---

## Access Points

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/

---

## Database

By default, the project uses **SQLite** (no setup needed). The database file will be created automatically at `D:\greweco-back\db.sqlite3`.

To use PostgreSQL instead:
1. Start PostgreSQL: `docker-compose up -d db`
2. Update `.env` file: Set `DATABASE_HOST=localhost`

---

## Troubleshooting

- **Backend not starting?** Check if port 8000 is available
- **Frontend not connecting?** Make sure backend is running on port 8000
- **Module errors?** Run `pip install -r requirements.txt` (backend) or `npm install` (frontend)

---

## Next Steps

1. ✅ Both servers running
2. ✅ Visit http://localhost:3000
3. ✅ Create account or login
4. ✅ Access admin at http://localhost:8000/admin/

