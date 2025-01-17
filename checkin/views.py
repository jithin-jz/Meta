from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Attendance
from datetime import timedelta

@login_required
def attendance_view(request):
    # Deletes old records (older than 30 days)
    Attendance.delete_old_records()

    if request.method == 'POST':
        # Clock In
        if 'clock_in' in request.POST and not Attendance.objects.filter(user=request.user, clock_out_time__isnull=True).exists():
            Attendance.objects.create(user=request.user, clock_in_time=timezone.now())
        
        # Clock Out
        elif 'clock_out' in request.POST:
            latest_attendance = Attendance.objects.filter(user=request.user, clock_out_time__isnull=True).last()
            if latest_attendance:
                latest_attendance.clock_out_time = timezone.now()
                latest_attendance.save()

        return redirect('attendance_view')

    # Display attendance records from the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)  
    attendances = Attendance.objects.filter(user=request.user, clock_in_time__gte=thirty_days_ago).order_by('-clock_in_time')

    return render(request, 'checkin.html', {'attendances': attendances})
