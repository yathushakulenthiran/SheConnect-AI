from django.db import models
from django.conf import settings
from django.utils import timezone


class Mentee(models.Model):
    """Mentee profile for the mentorship platform"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentee_profile')
    
    # Business Information
    business_stage = models.CharField(
        max_length=50,
        choices=[
            ('idea', 'Idea Stage'),
            ('startup', 'Startup Stage'),
            ('growth', 'Growth Stage'),
            ('established', 'Established Business'),
        ]
    )
    industry = models.CharField(max_length=100)
    business_name = models.CharField(max_length=200, blank=True)
    
    # Challenges and Goals
    main_challenges = models.TextField(help_text="Describe your main business challenges")
    mentorship_goals = models.TextField(help_text="What do you hope to achieve through mentorship?")
    
    # Personal Information
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_profile = models.URLField(blank=True)
    
    # Onboarding fields
    onboarding_complete = models.BooleanField(default=False)
    years_in_business = models.IntegerField(blank=True, null=True)
    team_size = models.IntegerField(blank=True, null=True)
    revenue_range = models.CharField(max_length=50, blank=True)
    preferred_meeting_mode = models.CharField(max_length=20, blank=True)
    languages = models.CharField(max_length=200, blank=True)
    
    # Profile Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mentees'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.business_stage}"


class ConnectionRequest(models.Model):
    """Connection requests between mentees and mentors"""
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE, related_name='connection_requests')
    mentor = models.ForeignKey('mentors.Mentor', on_delete=models.CASCADE, related_name='connection_requests')
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    
    message = models.TextField(blank=True, help_text="Optional message to the mentor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'connection_requests'
        ordering = ['-created_at']
        unique_together = ['mentee', 'mentor']

    def __str__(self):
        return f"{self.mentee.user.email} → {self.mentor.name} ({self.status})"


class MentorshipSession(models.Model):
    """Mentorship sessions between mentees and mentors"""
    connection = models.ForeignKey(ConnectionRequest, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    session_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled'
    )
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mentorship_sessions'
        ordering = ['-session_date']

    def __str__(self):
        return f"{self.title} - {self.connection.mentor.name}"
