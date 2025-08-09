from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]


