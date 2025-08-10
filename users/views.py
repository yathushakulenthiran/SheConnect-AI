from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import UserSignupForm


User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            # For demo purposes, make account active immediately
            user.is_active = True
            user.save()
            
            # Auto-login the user after signup
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Account created successfully! Welcome to SheConnect AI.")
            return redirect('mentees:register')
    else:
        form = UserSignupForm()
    return render(request, 'users/signup.html', { 'form': form })


def custom_login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to authenticate with username first
        user = authenticate(request, username=username_or_email, password=password)
        
        # If that fails, try with email
        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('mentees:dashboard')
        else:
            messages.error(request, "Invalid username/email or password.")
    
    return render(request, 'users/login.html')


def custom_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('core:home')


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Specify backend explicitly because multiple backends are configured
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, "Email verified. Welcome!")
        return redirect('mentees:register')
    messages.error(request, "Invalid or expired link.")
    return redirect('core:home')
