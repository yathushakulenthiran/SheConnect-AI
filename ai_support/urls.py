from django.urls import path
from . import views

app_name = 'ai_support'

urlpatterns = [
    path('chat/', views.mental_health_chat, name='chat'),
    path('resources/', views.mental_health_resources, name='resources'),
    path('matching/', views.ai_matching, name='matching'),
]
