from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    """Home page for SheConnect AI"""
    context = {
        'app_name': 'SheConnect AI',
        'description': 'Your AI-powered connection platform',
        'services': [
            {'name': 'AI Chat', 'description': 'Intelligent conversations'},
            {'name': 'Image Generation', 'description': 'Create stunning visuals'},
            {'name': 'Text Analysis', 'description': 'Advanced text processing'},
        ]
    }
    return render(request, 'core/home.html', context)


def health(request):
    """Health check endpoint"""
    return JsonResponse({
        "status": "ok", 
        "app": "SheConnect AI",
        "version": "1.0.0",
        "database": "connected"
    })
