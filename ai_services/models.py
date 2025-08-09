from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class AIService(models.Model):
    """Available AI services in the platform"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    service_type = models.CharField(
        max_length=50,
        choices=[
            ('chat', 'Chat'),
            ('image_gen', 'Image Generation'),
            ('text_gen', 'Text Generation'),
            ('analysis', 'Analysis'),
            ('translation', 'Translation'),
        ]
    )
    is_active = models.BooleanField(default=True)
    rate_limit = models.IntegerField(default=100)  # requests per hour
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ai_services'

    def __str__(self):
        return self.name


class Conversation(models.Model):
    """User conversations with AI"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=200, blank=True)
    service = models.ForeignKey(AIService, on_delete=models.CASCADE, related_name='conversations')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.email} - {self.title or 'Untitled'}"


class Message(models.Model):
    """Individual messages in conversations"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    role = models.CharField(
        max_length=20,
        choices=[
            ('user', 'User'),
            ('assistant', 'Assistant'),
            ('system', 'System'),
        ]
    )
    tokens_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.conversation.title} - {self.role}"


class UserServiceUsage(models.Model):
    """Track user usage of AI services"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_usage')
    service = models.ForeignKey(AIService, on_delete=models.CASCADE, related_name='usage')
    requests_count = models.IntegerField(default=0)
    tokens_used = models.IntegerField(default=0)
    last_used = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_service_usage'
        unique_together = ['user', 'service']

    def __str__(self):
        return f"{self.user.email} - {self.service.name}"
