from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mentee, ConnectionRequest


@login_required
def mentee_register(request):
    """Mentee registration and onboarding"""
    if request.method == 'POST':
        # Handle registration form
        pass
    
    context = {
        'title': 'Mentee Registration',
    }
    return render(request, 'mentees/register.html', context)


@login_required
def mentee_dashboard(request):
    """Mentee dashboard"""
    try:
        mentee = request.user.mentee_profile
    except Mentee.DoesNotExist:
        return redirect('mentees:register')
    
    # Get pending connections
    pending_connections = ConnectionRequest.objects.filter(
        mentee=mentee, 
        status='pending'
    )
    
    # Get accepted connections
    accepted_connections = ConnectionRequest.objects.filter(
        mentee=mentee, 
        status='accepted'
    )
    
    context = {
        'mentee': mentee,
        'pending_connections': pending_connections,
        'accepted_connections': accepted_connections,
    }
    return render(request, 'mentees/dashboard.html', context)


@login_required
def mentee_profile(request):
    """Mentee profile management"""
    try:
        mentee = request.user.mentee_profile
    except Mentee.DoesNotExist:
        return redirect('mentees:register')
    
    context = {
        'mentee': mentee,
    }
    return render(request, 'mentees/profile.html', context)


@login_required
def connection_requests(request):
    """Connection requests management"""
    try:
        mentee = request.user.mentee_profile
    except Mentee.DoesNotExist:
        return redirect('mentees:register')
    
    connections = ConnectionRequest.objects.filter(mentee=mentee)
    
    context = {
        'connections': connections,
    }
    return render(request, 'mentees/connections.html', context)
