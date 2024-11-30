from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'username', 'age', 'date_joined', 'can_be_contacted', 'can_data_be_shared',
                    'is_superuser', 'is_active',)
    list_filter = ('date_joined', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'age', 'can_be_contacted',
                       'can_data_be_shared', 'is_superuser', 'is_active')
        }),
    )
    search_fields = ('username',)
    ordering = ('date_joined',)


admin.site.register(User, CustomUserAdmin)
