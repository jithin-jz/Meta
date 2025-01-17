from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Leave
from django.utils.dateparse import parse_date

def leave(request):
    leave_requests = Leave.objects.filter(user=request.user).order_by('-start_date')

    if request.method == 'POST':
        leave_type = request.POST.get('leaveType')
        start_date = parse_date(request.POST.get('startDate'))
        end_date = parse_date(request.POST.get('endDate'))
        reason = request.POST.get('reason')

        if not all([leave_type, start_date, end_date, reason]):
            messages.error(request, 'All fields are required.')
            return render(request, 'leave.html', {'leave_requests': leave_requests})

        total_leave_days = (end_date - start_date).days + 1

        if total_leave_days < 1:
            messages.error(request, 'End date should be after start date.')
            return render(request, 'leave.html', {'leave_requests': leave_requests})

        latest_leave = Leave.objects.filter(user=request.user).latest('id') if Leave.objects.filter(user=request.user).exists() else None
        remaining_leave = latest_leave.remaining_leave if latest_leave else 10

        if total_leave_days <= remaining_leave:
            Leave.objects.create(
                user=request.user,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                remaining_leave=remaining_leave - total_leave_days
            )
            messages.success(request, 'Leave application submitted successfully.')
            return redirect('leave')

        messages.error(request, f'Insufficient leave balance. You have {remaining_leave} days remaining.')

    return render(request, 'leave.html', {'leave_requests': leave_requests})


def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'approved'
    leave.save()
    messages.success(request, f"Leave request for {leave.user.username} has been approved.")
    return redirect('admin_dashboard')


def reject_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)

    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason')

        if not rejection_reason:
            messages.error(request, "Please provide a reason for rejecting the leave request.")
            return render(request, 'reject_leave.html', {'leave': leave})

        leave.status = 'rejected'
        leave.rejection_reason = rejection_reason
        leave.save()

        messages.error(request, f"Leave request for {leave.user.username} has been rejected.")
        return redirect('admin_dashboard')

    return render(request, 'reject_leave.html', {'leave': leave})
