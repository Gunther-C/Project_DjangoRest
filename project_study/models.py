from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=8192)
    choice_type = [('back-end', 'Back-end'), ('front-end', 'Front-end'), ('ios', 'IOS'), ('android', 'Android')]
    type = models.CharField(max_length=50, choices=choice_type)
    date_joined = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator_project')

    def __str__(self):
        return self.name

    # a faire dans la vue
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Contributor.objects.get_or_create(user=self.author, project=self, defaults={'role': 'Author'})


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributor_project')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='project_shared')
    role = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}, {self.project.name}, {self.role}"
