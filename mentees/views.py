from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Mentee, ConnectionRequest
from .forms import MenteeRegistrationForm, MenteeOnboardingForm
from mentors.models import Mentor
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
    
    # Get all connection types
    pending_connections = ConnectionRequest.objects.filter(
        mentee=mentee, 
        status='pending'
    )
    
    accepted_connections = ConnectionRequest.objects.filter(
        mentee=mentee, 
        status='accepted'
    )
    
    rejected_connections = ConnectionRequest.objects.filter(
        mentee=mentee, 
        status='rejected'
    )
    
    context = {
        'pending_connections': pending_connections,
        'accepted_connections': accepted_connections,
        'rejected_connections': rejected_connections,
    }
    return render(request, 'mentees/connections.html', context)


@login_required
def send_connection_request(request, mentor_id):
    """Send a connection request to a mentor"""
    try:
        mentee = request.user.mentee_profile
    except Mentee.DoesNotExist:
        return redirect('mentees:register')
    
    mentor = get_object_or_404(Mentor, id=mentor_id, is_active=True)
    
    # Check if connection already exists
    existing_connection = ConnectionRequest.objects.filter(
        mentee=mentee, 
        mentor=mentor
    ).first()
    
    if existing_connection:
        if existing_connection.status == 'pending':
            messages.warning(request, 'Connection request already pending.')
        elif existing_connection.status == 'accepted':
            messages.info(request, 'You are already connected with this mentor.')
        elif existing_connection.status == 'rejected':
            messages.warning(request, 'Connection was previously rejected.')
        return redirect('mentors:detail', mentor_id=mentor_id)
    
    if request.method == 'POST':
        message = request.POST.get('message', '')
        
        # Create connection request
        connection = ConnectionRequest.objects.create(
            mentee=mentee,
            mentor=mentor,
            message=message
        )
        
        messages.success(request, f'Connection request sent to {mentor.name}!')
        return redirect('mentees:connections')
    
    context = {
        'mentor': mentor,
        'mentee': mentee,
    }
    return render(request, 'mentees/send_connection.html', context)

@login_required
def cancel_connection_request(request, connection_id):
    """Cancel a pending connection request"""
    try:
        mentee = request.user.mentee_profile
    except Mentee.DoesNotExist:
        return redirect('mentees:register')
    
    connection = get_object_or_404(ConnectionRequest, id=connection_id, mentee=mentee)
    
    if connection.status == 'pending':
        connection.delete()
        messages.success(request, 'Connection request cancelled.')
    else:
        messages.warning(request, 'Cannot cancel non-pending requests.')
    
    return redirect('mentees:connections')
