from django.db import models
from django.conf import settings
import uuid


class Project(models.Model):
    TYPE_CHOICES = [('back-end', 'Back-end'), ('front-end', 'Front-end'), ('ios', 'IOS'), ('android', 'Android')]

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=8200)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_author')

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_contributor')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_shared')
    role = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}, {self.project.name}, {self.role}"


class Issue(models.Model):
    TAG_CHOICES = [('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')]
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]
    STATUS_CHOICES = [('TO_DO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('FINISHED', 'Finished')]

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=8200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issue_author')

    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='assigned_issues', null=True, blank=True)

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='LOW')
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default='TASK')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='TO_DO')

    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # primary_key vs unique
    description = models.TextField(max_length="12400")
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comment")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_author")
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Auteur {self.author.username} issue {self.issue.title}"
