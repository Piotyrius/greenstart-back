#!/usr/bin/env python
"""
Create admin user for GREWECO platform
Username: admin
Password: admin
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greweco_back.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin_user():
    """Create or update admin user with full permissions."""
    username = 'admin'
    password = 'admin'
    email = 'admin@greweco.com'
    
    # Get or create user
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        }
    )
    
    # Update user to ensure full permissions
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password(password)
    user.save()
    
    if created:
        print("Admin user created successfully!")
    else:
        print("Admin user updated successfully!")
    
    print("\nLogin Credentials:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   Email: {email}")
    print("\nAccess URLs:")
    print("   Django Admin: http://localhost:8000/admin/")
    print("   API Login: http://localhost:8000/api/auth/login/")
    print("   Frontend: http://localhost:3000")
    print("\nUser has full permissions:")
    print(f"   - Django Admin access: {user.is_staff}")
    print(f"   - Superuser permissions: {user.is_superuser}")
    print(f"   - Active account: {user.is_active}")
    
    return user

if __name__ == '__main__':
    create_admin_user()

