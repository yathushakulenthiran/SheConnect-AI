from django.contrib import admin
from .models import AIService, Conversation, Message, UserServiceUsage


@admin.register(AIService)
class AIServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'is_active', 'rate_limit', 'created_at')
    list_filter = ('service_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'service', 'is_active', 'created_at', 'message_count')
    list_filter = ('is_active', 'service', 'created_at')
    search_fields = ('title', 'user__email', 'user__username')
    ordering = ('-updated_at',)
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'role', 'content_preview', 'tokens_used', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content', 'conversation__title')
    ordering = ('-created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(UserServiceUsage)
class UserServiceUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'requests_count', 'tokens_used', 'last_used')
    list_filter = ('service', 'last_used')
    search_fields = ('user__email', 'user__username', 'service__name')
    ordering = ('-last_used',)
