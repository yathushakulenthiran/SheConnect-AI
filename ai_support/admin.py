from django.contrib import admin
from .models import MentalHealthSession, AIMatchingScore, MentalHealthResource, ChatMessage


@admin.register(MentalHealthSession)
class MentalHealthSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_type', 'mood_rating', 'stress_level', 'created_at')
    list_filter = ('session_type', 'mood_rating', 'stress_level', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'notes')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Session Information', {
            'fields': ('user', 'session_type', 'mood_rating', 'stress_level')
        }),
        ('Content', {
            'fields': ('notes', 'ai_response')
        }),
    )
    
    readonly_fields = ('created_at',)


@admin.register(AIMatchingScore)
class AIMatchingScoreAdmin(admin.ModelAdmin):
    list_display = ('mentee', 'mentor', 'overall_score', 'business_stage_match', 'industry_match', 'created_at')
    list_filter = ('overall_score', 'created_at')
    search_fields = ('mentee__user__email', 'mentor__name')
    ordering = ('-overall_score',)
    
    fieldsets = (
        ('Matching Details', {
            'fields': ('mentee', 'mentor', 'overall_score')
        }),
        ('Individual Scores', {
            'fields': ('business_stage_match', 'industry_match', 'challenge_expertise_match', 'goal_alignment_match')
        }),
        ('AI Reasoning', {
            'fields': ('matching_reasoning',)
        }),
    )
    
    readonly_fields = ('created_at',)


@admin.register(MentalHealthResource)
class MentalHealthResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'location', 'contact_info')
    ordering = ('category', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Contact Information', {
            'fields': ('contact_info', 'location', 'website', 'phone', 'email')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('created_at',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'role', 'content_preview', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content', 'session__user__email')
    ordering = ('-created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('session', 'role', 'content')
        }),
    )
    
    readonly_fields = ('created_at',)
