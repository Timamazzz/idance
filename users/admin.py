from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'email', 'first_name', 'last_name', 'patronymic')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name', 'patronymic')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'date_joined')
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'patronymic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password1', 'password2')}
         ),
    )
    ordering = ('phone_number',)


admin.site.register(CustomUser, CustomUserAdmin)
