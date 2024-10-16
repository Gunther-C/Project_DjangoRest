from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'username', 'email', 'age', 'date_joined', 'can_be_contacted', 'can_data_be_shared',
                    'is_superuser', 'is_active',)
    list_filter = ('date_joined', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'username', 'email', 'password1', 'password2', 'age', 'date_joined', 'can_be_contacted',
                       'can_data_be_shared', 'is_superuser', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('date_joined',)


admin.site.register(User, CustomUserAdmin)