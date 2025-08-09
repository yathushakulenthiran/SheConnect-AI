from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mentee, ConnectionRequest
from .forms import MenteeRegistrationForm, MenteeOnboardingForm
from django import forms


@login_required
def mentee_register(request):
    """Mentee registration and onboarding"""
    try:
        mentee = request.user.mentee_profile
        return redirect('mentees:dashboard')
    except Mentee.DoesNotExist:
        mentee = None

    if request.method == 'POST':
        form = MenteeRegistrationForm(request.POST)
        if form.is_valid():
            mentee: Mentee = form.save(commit=False)
            mentee.user = request.user
            mentee.save()
            return redirect('mentees:dashboard')
    else:
        form = MenteeRegistrationForm()
    
    context = {
        'title': 'Mentee Registration',
        'form': form,
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
    
    class ProfileForm(MenteeRegistrationForm):
        class Meta(MenteeRegistrationForm.Meta):
            pass

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=mentee)
        if form.is_valid():
            form.save()
            return redirect('mentees:dashboard')
    else:
        form = ProfileForm(instance=mentee)

    return render(request, 'mentees/profile.html', { 'form': form, 'mentee': mentee })


@login_required
def mentee_onboarding(request):
    try:
        mentee = request.user.mentee_profile
    except Mentee.DoesNotExist:
        return redirect('mentees:register')
    if request.method == 'POST':
        form = MenteeOnboardingForm(request.POST, instance=mentee)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.onboarding_complete = True
            obj.save()
            return redirect('mentees:dashboard')
    else:
        form = MenteeOnboardingForm(instance=mentee)
    return render(request, 'mentees/onboarding.html', { 'form': form })


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
