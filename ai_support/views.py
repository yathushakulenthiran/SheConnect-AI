from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MentalHealthResource, MentalHealthSession
from mentees.models import Mentee
from .services import top_matches


@login_required
def mental_health_chat(request):
    """Mental health support chatbot"""
    if request.method == 'POST':
        # Handle chat interaction
        pass
    
    # Get user's recent sessions
    recent_sessions = MentalHealthSession.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'recent_sessions': recent_sessions,
    }
    return render(request, 'ai_support/chat.html', context)


def mental_health_resources(request):
    """Mental health resources directory"""
    resources = MentalHealthResource.objects.filter(is_active=True)
    
    # Filter by category
    category = request.GET.get('category', '')
    if category:
        resources = resources.filter(category=category)
    
    context = {
        'resources': resources,
        'category_filter': category,
    }
    return render(request, 'ai_support/resources.html', context)


@login_required
def ai_matching(request):
    """AI-powered mentor matching"""
    try:
        mentee = request.user.mentee_profile
    except Mentee.DoesNotExist:
        mentee = None

    results = []
    if mentee:
        results = top_matches(mentee)

    context = {
        'title': 'AI Mentor Matching',
        'results': results,
        'mentee': mentee,
    }
    return render(request, 'ai_support/matching.html', context)
