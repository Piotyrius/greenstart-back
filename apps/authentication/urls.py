from django.urls import path
from apps.authentication.views import register, login, refresh_token

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('refresh/', refresh_token, name='refresh'),
]

