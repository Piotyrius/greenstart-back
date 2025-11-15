# ⚡ Quick Start - Run Locally in 2 Minutes

## 🎯 Fastest Way to Run

### Step 1: Start Backend

**Windows:**
```bash
cd D:\greweco-back
run_local.bat
```

**Linux/Mac:**
```bash
cd D:\greweco-back
chmod +x run_local.sh && ./run_local.sh
```

Wait for: `Starting development server at http://127.0.0.1:8000/`

### Step 2: Start Frontend (New Terminal)

**Windows:**
```bash
cd D:\greweco-front
run_local.bat
```

**Linux/Mac:**
```bash
cd D:\greweco-front
chmod +x run_local.sh && ./run_local.sh
```

Wait for: `Ready - started server on 0.0.0.0:3000`

---

## ✅ Done!

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Admin:** http://localhost:8000/admin/

---

## 🎉 What Just Happened?

1. ✅ Backend created virtual environment
2. ✅ Installed Python dependencies
3. ✅ Created SQLite database (no PostgreSQL needed!)
4. ✅ Ran migrations
5. ✅ Started Django server on port 8000
6. ✅ Frontend installed Node dependencies
7. ✅ Started Next.js on port 3000

---

## 🔧 First Time Setup

### Create Admin User:

1. Stop backend (Ctrl+C)
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Enter username, email, password
4. Restart backend: `run_local.bat`

### Access Admin Panel:

- Go to: http://localhost:8000/admin/
- Login with superuser credentials
- Create test data (Buyers, Plantations, etc.)

---

## 🐛 Troubleshooting

**Backend won't start?**
- Check Python is installed: `python --version`
- Check port 8000 is free
- Try: `python manage.py check`

**Frontend won't start?**
- Check Node.js is installed: `node --version`
- Check port 3000 is free
- Try: `npm install` then `npm run dev`

**Can't connect to API?**
- Make sure backend is running on port 8000
- Check `.env.local` in frontend has: `NEXT_PUBLIC_API_URL=http://localhost:8000`

---

## 📝 Notes

- **Database:** Uses SQLite by default (file: `db.sqlite3`)
- **No PostgreSQL needed** for local development
- **Auto-reload:** Both servers auto-reload on file changes
- **Hot-reload:** Frontend has hot module replacement

---

## 🚀 Next Steps

1. Visit http://localhost:3000
2. Register a new account
3. Or login to admin panel
4. Start building! 🎉

