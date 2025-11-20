from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LoginLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'phone_number', 'date_of_birth', 'address')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'phone_number', 'date_of_birth', 'address', 'email', 'first_name', 'last_name')
        }),
    )


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'login_time', 'success']
    list_filter = ['success', 'login_time']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'ip_address', 'user_agent', 'login_time', 'success']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

