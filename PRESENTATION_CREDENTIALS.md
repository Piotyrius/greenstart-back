# GREWECO Presentation - Admin Credentials

## 🔐 Admin User Credentials

**Username:** `admin`  
**Password:** `admin`  
**Email:** `admin@greweco.com`

---

## 🔗 Access URLs

### Backend (Django)
- **Django Admin Panel**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/
- **API Login**: http://localhost:8000/api/auth/login/

### Frontend (Next.js)
- **Frontend Application**: http://localhost:3000
- **Login Page**: http://localhost:3000/login

---

## ✅ User Permissions

The admin user has **FULL PERMISSIONS**:
- ✅ Django Admin access (is_staff = True)
- ✅ Superuser permissions (is_superuser = True)
- ✅ Active account (is_active = True)
- ✅ Can access all API endpoints
- ✅ Can manage all models in Django admin
- ✅ Can create/edit/delete any data

---

## 🚀 Quick Login Steps

### 1. Django Admin Panel
1. Go to: http://localhost:8000/admin/
2. Username: `admin`
3. Password: `admin`
4. Click "Log in"

### 2. Frontend Login
1. Go to: http://localhost:3000/login
2. Username: `admin`
3. Password: `admin`
4. Click "Login"

### 3. API Login (for testing)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

Response will include JWT tokens:
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@greweco.com"
  },
  "tokens": {
    "refresh": "...",
    "access": "..."
  }
}
```

---

## 📋 What You Can Do

### Django Admin Panel
- View all models (Buyers, Plantations, Tree Lots, Purchases, NFT Certificates)
- Create/edit/delete any data
- Manage users
- View system information

### Frontend
- Access all dashboard pages
- View plantations
- Manage buyers (B2B/B2C)
- View NFT certificates
- Access analytics

### API
- All endpoints accessible with JWT token
- Full CRUD operations
- Create test data via API

---

## 🔄 Recreate Admin User

If you need to recreate the admin user:

```powershell
cd D:\greweco-back
python create_admin_user.py
```

Or manually:
```powershell
python manage.py shell
```

Then in Python shell:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
user, created = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@greweco.com', 'is_staff': True, 'is_superuser': True}
)
user.set_password('admin')
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()
```

---

## 🎯 Presentation Checklist

- [x] Admin user created
- [x] Full permissions granted
- [x] Django admin accessible
- [x] Frontend login works
- [x] API authentication works
- [ ] Create sample data (optional)
- [ ] Test all features

---

## 📝 Notes

- **Security**: This is a test/demo account. Change password in production!
- **Permissions**: Admin has all permissions by default
- **Access**: Works for both frontend and backend
- **JWT Tokens**: Valid for API authentication

---

## 🆘 Troubleshooting

**Can't login to Django admin?**
- Check if user exists: `python manage.py shell` → `User.objects.get(username='admin')`
- Recreate user: `python create_admin_user.py`

**Frontend login fails?**
- Check backend is running: http://localhost:8000/api/
- Check CORS settings in backend
- Check browser console for errors

**API returns 401?**
- Get JWT token from login endpoint
- Include token in headers: `Authorization: Bearer <token>`

