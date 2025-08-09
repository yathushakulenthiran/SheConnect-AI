from django.contrib import admin
from .models import Mentee, ConnectionRequest, MentorshipSession


@admin.register(Mentee)
class MenteeAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_stage', 'industry', 'business_name', 'is_active', 'created_at')
    list_filter = ('business_stage', 'industry', 'is_active', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'business_name', 'industry')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone', 'location', 'linkedin_profile')
        }),
        ('Business Information', {
            'fields': ('business_stage', 'industry', 'business_name')
        }),
        ('Mentorship Goals', {
            'fields': ('main_challenges', 'mentorship_goals')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ('mentee', 'mentor', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('mentee__user__email', 'mentor__name', 'message')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Connection Details', {
            'fields': ('mentee', 'mentor', 'status', 'message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'connection', 'session_date', 'duration_minutes', 'status')
    list_filter = ('status', 'session_date', 'created_at')
    search_fields = ('title', 'description', 'connection__mentor__name', 'connection__mentee__user__email')
    ordering = ('-session_date',)
    
    fieldsets = (
        ('Session Details', {
            'fields': ('connection', 'title', 'description', 'session_date', 'duration_minutes')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
