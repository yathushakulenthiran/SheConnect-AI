from django.urls import path
from . import views

app_name = 'ai_support'

urlpatterns = [
    path('chat/', views.mental_health_chat, name='chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('matching/', views.ai_matching, name='matching'),
    path('mood-analytics/', views.mood_analytics, name='mood_analytics'),
]


