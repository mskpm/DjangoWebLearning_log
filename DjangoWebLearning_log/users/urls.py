"""Definiuje wzorce adresów URL dla users"""

from django.urls import path, re_path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'users'

urlpatterns = [
    # Strona logowania
    path('login/', LoginView.as_view(template_name='users/login.html'), name="login"),
    # Strona wylogowania
    path('logout/', views.logout_view, name="logout"),
    # Strona rejestracji
    path('register/', views.register, name="register"),
    ]
