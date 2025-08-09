from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify'),
]


