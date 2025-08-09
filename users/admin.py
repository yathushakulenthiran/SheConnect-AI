from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_verified', 'subscription_tier')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 'profile__subscription_tier')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'profile_picture', 'bio', 'date_of_birth', 'is_verified')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'profile_picture', 'bio', 'date_of_birth', 'is_verified')}),
    )

    def subscription_tier(self, obj):
        return obj.profile.subscription_tier if hasattr(obj, 'profile') else 'N/A'
    subscription_tier.short_description = 'Subscription'


admin.site.register(User, CustomUserAdmin)
