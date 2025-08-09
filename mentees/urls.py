from django.urls import path
from . import views

app_name = 'mentees'

urlpatterns = [
    path('register/', views.mentee_register, name='register'),
    path('dashboard/', views.mentee_dashboard, name='dashboard'),
    path('profile/', views.mentee_profile, name='profile'),
    path('connections/', views.connection_requests, name='connections'),
]
