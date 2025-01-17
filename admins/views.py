from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime
from django.utils.timezone import make_aware
from calendar import monthrange
from account.models import UserProfile
from leave.models import Leave
from .models import Events
from django.http import JsonResponse
from django.db.models import Q

@login_required
def admin_dashboard(request):
    profiles = UserProfile.objects.all()
    leaves = Leave.objects.all()
    current_time = timezone.now()
    events = Events.objects.filter(date__gte=current_time).order_by('date')

    context = {
        'profiles': profiles,
        'leaves': leaves,
        'events': events,
    }
    return render(request, 'admin.html', context)

@login_required
def add_employee(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        salary = request.POST['salary']
        position = request.POST['position']

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, salary=salary, position=position)
        messages.success(request, "Employee added successfully.")
        return redirect('admin_dashboard')

    return render(request, 'admin.html')

@login_required
def edit_employee(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    if request.method == 'POST':
        profile.position = request.POST['position']
        profile.salary = request.POST['salary']
        profile.save()
        messages.success(request, "Employee updated successfully.")
        return redirect('admin_dashboard')

    return render(request, 'admin.html', {'profile': profile})

@login_required
def delete_employee(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    user = profile.user
    profile.delete()
    user.delete()
    messages.success(request, "Employee deleted successfully.")
    return redirect('admin_dashboard')

@login_required
def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'approved'
    leave.save()
    messages.success(request, f"Leave request for {leave.user.username} has been approved.")
    return redirect('admin_dashboard')

@login_required
def reject_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    
    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason')
        
        if rejection_reason:
            leave.status = 'rejected'
            leave.rejection_reason = rejection_reason
            leave.save()
            messages.error(request, f"Leave request for {leave.user.username} has been rejected with a reason.")
        else:
            messages.error(request, "Rejection reason is required.")
        return redirect('admin_dashboard')

    return render(request, 'admin.html', {'leave': leave})

@login_required
def events(request):
    today = timezone.now().date()

    # Add New Event
    if request.method == 'POST' and 'name' in request.POST:
        name = request.POST['name']
        category = request.POST['category']
        date_str = request.POST['date']
        time_str = request.POST['time']

        if name and category and date_str and time_str:
            date = parse_date(date_str)
            time = datetime.strptime(time_str, '%H:%M').time()
            if date:
                event_datetime = make_aware(datetime.combine(date, time))
                Events.objects.create(
                    user=request.user,
                    name=name,
                    category=category,
                    date=event_datetime.date(),
                    time=event_datetime.time()
                )
                return redirect('admin_dashboard')

    # Delete Event
    if request.method == 'POST' and 'delete_event' in request.POST:
        event_id = request.POST.get('delete_event')
        event = get_object_or_404(Events, id=event_id, user=request.user)
        event.delete()
        return redirect('admin_dashboard')

    # Calculate calendar days for the current month
    start_date = today.replace(day=1)
    _, last_day = monthrange(today.year, today.month)
    end_date = today.replace(day=last_day)

    # Get events for the current month
    events = Events.objects.filter(user=request.user, date__range=[start_date, end_date])

    # Generate calendar days with events
    calendar_days = []
    for day in range(1, last_day + 1):
        current_day = today.replace(day=day)
        day_events = events.filter(date=current_day)
        calendar_days.append({
            'day': day,
            'events': day_events,
            'today': current_day == today,
            'current_month': True,
        })

    context = {
        'events': events,
        'today': today,
        'calendar_days': calendar_days,
    }

    return render(request, 'admin.html', context)

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('admin_dashboard')


#chat
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from account.models import UserProfile
from .models import Message

@login_required
def chat(request, user_id=None):
    if user_id:
        recipient = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            content = request.POST.get('content')
            if content:
                Message.objects.create(sender=request.user, recipient=recipient, content=content)
                return JsonResponse({'success': True, 'message': 'Message sent successfully.'})

        # Retrieve messages between the logged-in user and the recipient
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=recipient)) |
            (Q(sender=recipient) & Q(recipient=request.user))
        ).order_by('timestamp')
        return render(request, 'chat.html', {'messages': messages, 'recipient': recipient})

    # If no specific user is selected, list all employees
    employees = UserProfile.objects.exclude(user=request.user)
    return render(request, 'chat.html', {'employees': employees})

