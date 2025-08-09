from django.db import models
from django.conf import settings
from django.utils import timezone


class MentalHealthSession(models.Model):
    """Mental health support sessions with AI chatbot"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mental_health_sessions')
    session_type = models.CharField(
        max_length=20,
        choices=[
            ('daily_checkin', 'Daily Check-in'),
            ('weekly_checkin', 'Weekly Check-in'),
            ('stress_support', 'Stress Support'),
            ('motivation', 'Motivational Content'),
            ('resources', 'Resource Request'),
        ]
    )
    mood_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)],
        help_text="Rate your mood from 1-10"
    )
    stress_level = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)],
        help_text="Rate your stress level from 1-10"
    )
    notes = models.TextField(blank=True)
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mental_health_sessions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.session_type} ({self.created_at.date()})"


class AIMatchingScore(models.Model):
    """AI matching scores between mentees and mentors"""
    mentee = models.ForeignKey('mentees.Mentee', on_delete=models.CASCADE, related_name='ai_matches')
    mentor = models.ForeignKey('mentors.Mentor', on_delete=models.CASCADE, related_name='ai_matches')
    
    # Matching criteria scores (0-100)
    business_stage_match = models.IntegerField(default=0)
    industry_match = models.IntegerField(default=0)
    challenge_expertise_match = models.IntegerField(default=0)
    goal_alignment_match = models.IntegerField(default=0)
    
    # Overall score
    overall_score = models.IntegerField(default=0)
    
    # AI reasoning
    matching_reasoning = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_matching_scores'
        ordering = ['-overall_score']
        unique_together = ['mentee', 'mentor']

    def __str__(self):
        return f"{self.mentee.user.email} ↔ {self.mentor.name} (Score: {self.overall_score})"

    def calculate_overall_score(self):
        """Calculate overall matching score"""
        weights = {
            'business_stage_match': 0.3,
            'industry_match': 0.25,
            'challenge_expertise_match': 0.25,
            'goal_alignment_match': 0.2,
        }
        
        total_score = 0
        for field, weight in weights.items():
            total_score += getattr(self, field) * weight
        
        self.overall_score = int(total_score)
        return self.overall_score


class MentalHealthResource(models.Model):
    """Local mental health resources for Sri Lanka"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('counseling', 'Counseling Services'),
            ('support_groups', 'Support Groups'),
            ('hotlines', 'Crisis Hotlines'),
            ('online_resources', 'Online Resources'),
            ('professional_help', 'Professional Help'),
        ]
    )
    contact_info = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mental_health_resources'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} - {self.category}"


class ChatMessage(models.Model):
    """Individual chat messages for mental health support"""
    session = models.ForeignKey(MentalHealthSession, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    role = models.CharField(
        max_length=20,
        choices=[
            ('user', 'User'),
            ('assistant', 'AI Assistant'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.session.user.email} - {self.role} ({self.created_at})"
