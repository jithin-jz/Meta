from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_projects")
    project_assign = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.project_name} - {self.user.username}"
