from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import SignupForm


User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            # send verification email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verify_url = request.build_absolute_uri(f"/users/verify/{uid}/{token}/")
            send_mail(
                subject="Verify your SheConnect account",
                message=f"Click to verify: {verify_url}",
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@sheconnect.ai'),
                recipient_list=[user.email],
                fail_silently=True,
            )
            messages.success(request, "Account created. Please check your email to verify.")
            return redirect('core:home')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', { 'form': form })


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
