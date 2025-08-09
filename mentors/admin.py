from django.contrib import admin
from .models import Mentor


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('name', 'expertise', 'years_experience', 'industry', 'availability_status', 'average_rating', 'rating_count', 'is_verified', 'is_active')
    list_filter = ('availability_status', 'is_verified', 'is_active', 'industry', 'business_stage_expertise', 'created_at')
    search_fields = ('name', 'expertise', 'email', 'short_bio')
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone', 'photo')
        }),
        ('Professional Details', {
            'fields': ('expertise', 'years_experience', 'industry', 'business_stage_expertise')
        }),
        ('Profile Content', {
            'fields': ('short_bio', 'key_focus_areas', 'linkedin_profile')
        }),
        ('Status', {
            'fields': ('availability_status', 'is_verified', 'is_active')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
