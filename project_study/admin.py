from django.contrib import admin
from .models import Project, Contributor


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'type', 'date_joined')
    list_filter = ('type', 'date_joined')
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Details', {'fields': ('author', 'type')}),

    )
    search_fields = ('name', 'author__username')
    ordering = ('date_joined',)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'user', 'role', 'created_date')
    list_filter = ('role', 'created_date')
    fieldsets = (
        (None, {'fields': ('project',)}),
        ('Details', {'fields': ('user', 'role')}),

    )
    ordering = ('created_date',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
