from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'last_name', 'first_name', 'is_premium', 'is_staff')
    list_filter = ('is_premium', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'username', 'last_name', 'first_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('追加情報', {'fields': ('phone_number', 'is_premium', 'stripe_customer_id')}),
    )