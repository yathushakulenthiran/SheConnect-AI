from django.shortcuts import render
from django.http import JsonResponse
from mentors.models import Mentor
from mentees.models import Mentee



def home(request):
    """Home page for SheConnect AI Mentorship Platform"""
    # Get featured mentors
    featured_mentors = Mentor.objects.filter(
        is_active=True, 
        is_verified=True,
        availability_status='available'
    )[:6]
    

    
    context = {
        'app_name': 'SheConnect AI',
        'tagline': 'AI-Powered Mentorship & Mental Health Support for Women Entrepreneurs',
        'description': 'Connect with experienced mentors, get AI-powered business guidance, and access mental health support designed for women entrepreneurs in Sri Lanka.',
        'featured_mentors': featured_mentors,

        'stats': {
            'mentors': Mentor.objects.filter(is_active=True).count(),
            'mentees': Mentee.objects.filter(is_active=True).count(),
            'connections': '100+',
            'success_stories': '50+'
        }
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page"""
    context = {
        'title': 'About SheConnect AI',
        'mission': 'Empowering women entrepreneurs in Sri Lanka through AI-powered mentorship and mental health support.',
        'vision': 'To create a supportive ecosystem where every woman entrepreneur has access to guidance, resources, and mental well-being support.',
    }
    return render(request, 'core/about.html', context)


def contact(request):
    """Contact page"""
    context = {
        'title': 'Contact Us',
        'email': 'hello@sheconnect.ai',
        'phone': '+94 11 234 5678',
        'address': 'Colombo, Sri Lanka',
    }
    return render(request, 'core/contact.html', context)


def health(request):
    """Health check endpoint"""
    return JsonResponse({
        "status": "ok",
        "app": "SheConnect AI Mentorship Platform",
        "version": "1.0.0",
        "database": "connected",
        "features": [
            "Mentor Directory",
            "AI Matching",
            "Mental Health Support",
            "Connection Management"
        ]
    })
