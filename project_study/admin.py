from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'author', 'type', 'created_date')
    list_filter = ('type', 'created_date')
    fieldsets = (
        ('Projet', {'fields': ('author',)}),
        ('Details', {'fields': ('name', 'description', 'type')}),
    )
    search_fields = ('name', 'author__username')
    ordering = ('created_date',)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'user', 'role', 'created_date')
    list_filter = ('role', 'created_date')
    fieldsets = (
        ('Projet', {'fields': ('project',)}),
        ('Details', {'fields': ('user', 'role')}),
    )
    ordering = ('created_date',)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'title', 'description', 'author', 'priority', 'tag', 'status',
                    'assigned_to', 'created_date')
    list_filter = ('priority', 'created_date')
    fieldsets = (
        ('Projet', {'fields': ('project',)}),
        ('Details', {'fields': ('title', 'description', 'author', 'assigned_to')}),
    )
    ordering = ('created_date',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'author', 'description')
    list_filter = ('issue', 'created_date')
    fieldsets = (
        ('Issue', {'fields': ('issue',)}),
        ('Details', {'fields': ('author', 'description')}),
    )
    ordering = ('created_date',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
