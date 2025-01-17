from django.db import models
from django.contrib.auth.models import User

class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick Leave'),
        ('personal', 'Personal Leave'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    remaining_leave = models.IntegerField(default=10)  # Default leave balance is 10 days
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(null=True, blank=True)  # Add rejection_reason field

    def calculate_days(self):
        """Calculates the number of leave days."""
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f'{self.user} - {self.leave_type}'

