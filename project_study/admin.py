from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'type', 'created_date', 'is_active')
    list_filter = ('type', 'created_date', 'is_active')
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Details', {'fields': ('author', 'type')}),
        ('Dates', {'fields': ('created_date', 'updated_date')}),
        ('Status', {'fields': ('is_active',)}),
    )
    search_fields = ('name', 'author__username')
    ordering = ('created_date',)


admin.site.register(Project, ProjectAdmin)
