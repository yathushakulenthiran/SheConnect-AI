from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Mentor(models.Model):
    """Mentor profile for the mentorship platform"""
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='mentor_photos/', blank=True, null=True)
    expertise = models.CharField(max_length=200)
    years_experience = models.IntegerField()
    short_bio = models.TextField()
    key_focus_areas = models.TextField()
    availability_status = models.CharField(
        max_length=20,
        choices=[
            ('available', 'Available'),
            ('busy', 'Busy'),
            ('unavailable', 'Unavailable'),
        ],
        default='available'
    )
    industry = models.CharField(max_length=100)
    business_stage_expertise = models.CharField(
        max_length=50,
        choices=[
            ('idea', 'Idea Stage'),
            ('startup', 'Startup Stage'),
            ('growth', 'Growth Stage'),
            ('established', 'Established Business'),
        ]
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_profile = models.URLField(blank=True)
    # Ratings
    average_rating = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mentors'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.expertise}"

    @property
    def full_expertise(self):
        return f"{self.expertise} ({self.years_experience} years experience)"
