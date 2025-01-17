from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    position = models.CharField(
        max_length=100,
        choices=[
            ('developer', 'Developer'),
            ('uiux', 'UI/UX Designer'),
            ('manager', 'Manager'),
            ('analyst', 'Analyst'),
        ],
        default='developer'
    )
    place = models.CharField(max_length=100, default='Unknown')
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    last_login_time = models.DateTimeField(blank=True, null=True)
    employee_id = models.CharField(max_length=20, unique=True, null=True)

    def save(self, *args, **kwargs):
        # Generate a unique employee ID if it's not already set
        if not self.employee_id:
            self.employee_id = self.generate_employee_id()
        super().save(*args, **kwargs)

    def generate_employee_id(self):
        # Generate a unique employee ID (you can customize this format)
        return f"EMP{uuid.uuid4().hex[:4].upper()}"

    def __str__(self):
        return self.user.username

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

