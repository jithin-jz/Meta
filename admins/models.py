from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Events(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)  
    category = models.CharField(max_length=50, null=True, blank=True)  
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)  

    def __str__(self):
        return f"{self.name} - {self.date} {self.time.strftime('%H:%M')}"


class Leaves(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ])
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
    
#chat
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"