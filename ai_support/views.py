import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import MentalHealthSession, ChatMessage
from mentees.models import Mentee
from .services import top_matches
from .chatbot_service import chatbot


@login_required
def mental_health_chat(request):
    """Mental health support chatbot with full functionality"""
    if request.method == 'POST':
        # Handle chat interaction
        message = request.POST.get('message', '').strip()
        mood_rating = request.POST.get('mood_rating', 5)
        stress_level = request.POST.get('stress_level', 5)
        
        if message:
            # Create or get current session
            session, created = MentalHealthSession.objects.get_or_create(
                user=request.user,
                session_type='daily_checkin',
                created_at__date=timezone.now().date(),
                defaults={
                    'mood_rating': mood_rating,
                    'stress_level': stress_level,
                    'notes': '',
                    'ai_response': ''
                }
            )
            
            # Update session if it already exists
            if not created:
                session.mood_rating = mood_rating
                session.stress_level = stress_level
                session.save()
            
            # Save user message
            ChatMessage.objects.create(
                session=session,
                content=message,
                role='user'
            )
            
            # Generate AI response for entrepreneurs
            ai_response = chatbot.generate_entrepreneur_response(message)
            
            # Save AI response
            ChatMessage.objects.create(
                session=session,
                content=ai_response,
                role='assistant'
            )
            
            # Update session with AI response
            session.ai_response = ai_response
            session.save()
            
            return JsonResponse({
                'response': ai_response,
                'mood_rating': mood_rating,
                'stress_level': stress_level
            })
    
    # Get user's recent sessions and mood trends
    recent_sessions = MentalHealthSession.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    # Get today's session if it exists
    today_session = None
    try:
        today_session = MentalHealthSession.objects.get(
            user=request.user,
            created_at__date=timezone.now().date()
        )
    except MentalHealthSession.DoesNotExist:
        pass
    
    # Get recent chat messages for display
    recent_messages = []
    if today_session:
        recent_messages = ChatMessage.objects.filter(
            session=today_session
        ).order_by('created_at')
    
    # Calculate mood trends
    session_data = []
    for session in recent_sessions:
        session_data.append({
            'mood_rating': session.mood_rating,
            'stress_level': session.stress_level,
            'date': session.created_at.date()
        })
    
    mood_trends = chatbot.track_mood_trends(session_data)
    
    context = {
        'recent_sessions': recent_sessions,
        'today_session': today_session,
        'recent_messages': recent_messages,
        'mood_trends': mood_trends,
        'current_mood': today_session.mood_rating if today_session else 5,
        'current_stress': today_session.stress_level if today_session else 5,
    }
    return render(request, 'ai_support/chat.html', context)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """AJAX endpoint for sending chat messages"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        mood_rating = data.get('mood_rating', 5)
        stress_level = data.get('stress_level', 5)
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Create or get current session
        session, created = MentalHealthSession.objects.get_or_create(
            user=request.user,
            session_type='daily_checkin',
            created_at__date=timezone.now().date(),
            defaults={
                'mood_rating': mood_rating,
                'stress_level': stress_level,
                'notes': '',
                'ai_response': ''
            }
        )
        
        # Update session if it already exists
        if not created:
            session.mood_rating = mood_rating
            session.stress_level = stress_level
            session.save()
        
        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            content=message,
            role='user'
        )
        
        # Generate AI response for entrepreneurs
        ai_response = chatbot.generate_entrepreneur_response(message)
        
        # Save AI response
        ai_message = ChatMessage.objects.create(
            session=session,
            content=ai_response,
            role='assistant'
        )
        
        # Update session with AI response
        session.ai_response = ai_response
        session.save()
        
        return JsonResponse({
            'success': True,
            'user_message': {
                'content': user_message.content,
                'timestamp': user_message.created_at.isoformat(),
                'role': user_message.role
            },
            'ai_response': {
                'content': ai_message.content,
                'timestamp': ai_message.created_at.isoformat(),
                'role': ai_message.role
            },
            'mood_rating': mood_rating,
            'stress_level': stress_level
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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


@login_required
def mood_analytics(request):
    """Mood tracking and analytics dashboard"""
    # Get user's mood history
    sessions = MentalHealthSession.objects.filter(
        user=request.user
    ).order_by('created_at')
    
    # Prepare data for charts
    mood_data = []
    stress_data = []
    dates = []
    
    for session in sessions:
        mood_data.append(session.mood_rating)
        stress_data.append(session.stress_level)
        dates.append(session.created_at.strftime('%Y-%m-%d'))
    
    # Calculate statistics
    if sessions:
        avg_mood = sum(session.mood_rating for session in sessions) / len(sessions)
        avg_stress = sum(session.stress_level for session in sessions) / len(sessions)
        total_sessions = len(sessions)
    else:
        avg_mood = 5
        avg_stress = 5
        total_sessions = 0
    
    # Get mood trends
    session_data = []
    for session in sessions:
        session_data.append({
            'mood_rating': session.mood_rating,
            'stress_level': session.stress_level,
            'date': session.created_at.date()
        })
    
    mood_trends = chatbot.track_mood_trends(session_data)
    
    context = {
        'mood_data': mood_data,
        'stress_data': stress_data,
        'dates': dates,
        'avg_mood': round(avg_mood, 1),
        'avg_stress': round(avg_stress, 1),
        'total_sessions': total_sessions,
        'mood_trends': mood_trends,
        'sessions': sessions[:10],  # Recent 10 sessions
    }
    return render(request, 'ai_support/mood_analytics.html', context)
