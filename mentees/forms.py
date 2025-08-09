from django import forms
from .models import Mentee


class MenteeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Mentee
        fields = [
            'business_stage',
            'industry',
            'business_name',
            'main_challenges',
            'mentorship_goals',
            'phone',
            'location',
            'linkedin_profile',
        ]
        widgets = {
            'main_challenges': forms.Textarea(attrs={'rows': 4}),
            'mentorship_goals': forms.Textarea(attrs={'rows': 4}),
        }


class MenteeOnboardingForm(forms.ModelForm):
    class Meta:
        model = Mentee
        fields = [
            'years_in_business',
            'team_size',
            'revenue_range',
            'preferred_meeting_mode',
            'languages',
        ]


