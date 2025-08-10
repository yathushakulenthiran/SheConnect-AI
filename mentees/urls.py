from django.urls import path
from . import views

app_name = 'mentees'

urlpatterns = [
    path('register/', views.mentee_register, name='register'),
    path('onboarding/', views.mentee_onboarding, name='onboarding'),
    path('dashboard/', views.mentee_dashboard, name='dashboard'),
    path('profile/', views.mentee_profile, name='profile'),
    path('connections/', views.connection_requests, name='connections'),
    path('connect/<int:mentor_id>/', views.send_connection_request, name='send_connection'),
    path('cancel-connection/<int:connection_id>/', views.cancel_connection_request, name='cancel_connection'),
]

