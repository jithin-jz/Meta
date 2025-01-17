from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='app_attendances')
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.clock_in_time}'

    def get_duration(self):
        """Returns the duration between clock in and clock out in hours."""
        if self.clock_out_time:
            duration = self.clock_out_time - self.clock_in_time
            return round(duration.total_seconds() / 3600, 2)
        return None

    @staticmethod
    def delete_old_records():
        """Delete records older than 30 days."""
        time_threshold = timezone.now() - timedelta(days=30)
        Attendance.objects.filter(clock_in_time__lt=time_threshold).delete()
