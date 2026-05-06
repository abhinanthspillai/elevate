from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('role', 'profile_image')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')

admin.site.register(User, CustomUserAdmin)
