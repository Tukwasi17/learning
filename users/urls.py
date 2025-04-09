"""Define URL pattern for users"""
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    #Include default authentication URL
    path('', include('django.contrib.auth.urls')),

    #user registration page
    path('register/', views.register, name='register'),

]
