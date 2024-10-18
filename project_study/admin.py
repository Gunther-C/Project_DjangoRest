from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'type', 'date_joined')
    list_filter = ('type', 'date_joined')
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Details', {'fields': ('author', 'type')}),
        ('Dates', {'fields': ('date_joined', 'create')}),
    )
    search_fields = ('name', 'author__username')
    ordering = ('date_joined',)


admin.site.register(Project, ProjectAdmin)
