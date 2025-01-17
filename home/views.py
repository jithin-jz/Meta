import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend suitable for web environments

import matplotlib.pyplot as plt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.utils import timezone
from io import BytesIO
import base64
import pytz

from account.models import UserProfile, Task
from admins.models import Events
from leave.models import Leave
from assign.models import Project


@login_required
def home(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    # Fetch remaining leave or set default leave balance
    leave_qs = Leave.objects.filter(user=request.user).order_by('-id')
    remaining_leave = leave_qs.first().remaining_leave if leave_qs.exists() else 10

    # Total number of employees
    total_employees = UserProfile.objects.count()

    # Fetch user's tasks
    tasks = Task.objects.filter(user=request.user)

    # Fetch upcoming events
    today = timezone.now().date()
    upcoming_events = Events.objects.filter(date__gte=today).order_by('date')

    # Fetch all assigned projects
    
    projects = Project.objects.filter(user=request.user)

    # Count distribution of employees by position
    position_distribution_qs = UserProfile.objects.values('position').annotate(count=Count('position'))
    position_distribution = {item['position'].capitalize(): item['count'] for item in position_distribution_qs}

    # Generate a pie chart for position distribution
    chart_data = create_pie_chart(position_distribution)

    # Handle POST requests for adding or deleting tasks
    if request.method == "POST":
        task_name = request.POST.get('name')
        delete_task_id = request.POST.get('delete_task_id')

        if task_name:
            Task.objects.create(user=request.user, name=task_name)
            messages.success(request, 'Task added successfully.')
        elif delete_task_id:
            task = get_object_or_404(Task, id=delete_task_id, user=request.user)
            task.delete()
            messages.success(request, 'Task deleted successfully.')

        return redirect('home')

    context = {
        'user': request.user,
        'profile': profile,
        'last_login_time': profile.last_login_time,
        'remaining_leave': remaining_leave,
        'total_employees': total_employees,
        'upcoming_events': upcoming_events,
        'tasks': tasks,
        'position_distribution': position_distribution,
        'chart_data': chart_data,
        'projects': projects,
    }

    return render(request, 'home.html', context)


def create_pie_chart(data):
    """Helper function to create and encode a pie chart."""
    positions = list(data.keys())
    counts = list(data.values())

    fig, ax = plt.subplots()
    ax.pie(counts, labels=positions, autopct='%1.1f%%', startangle=90, 
           colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is drawn as a circle

    # Save chart to a bytes buffer and encode it for display
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)  # Close the figure to release memory

    return chart_data


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        position = request.POST.get('position').strip()
        place = request.POST.get('place').strip()

        # Validation checks
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
        elif not all([username, email, password, position, place]):
            messages.error(request, 'All fields are required.')
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                UserProfile.objects.create(user=user, position=position, place=place)
                messages.success(request, 'Registration successful. Please log in.')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'An error occurred during registration.')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

        return redirect('register')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)

            # Update last login time
            update_last_login_time(user)

            # Redirect based on username
            return redirect('admin_dashboard' if user.username == 'admin' else 'home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def update_last_login_time(user):
    """Helper function to update last login time with timezone adjustment."""
    user_profile = get_object_or_404(UserProfile, user=user)
    india_tz = pytz.timezone('Asia/Kolkata')
    user_profile.last_login_time = timezone.now().astimezone(india_tz)
    user_profile.save()


@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'profile.html', {'profile': user_profile})


@login_required
def tasks(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Task.objects.create(user=request.user, name=name)
            return redirect('home')

    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('home')


@login_required
def approve_leave(request, leave_id):
    update_leave_status(leave_id, 'approved')
    messages.success(request, 'Leave application approved.')
    return redirect('home')


@login_required
def reject_leave(request, leave_id):
    update_leave_status(leave_id, 'rejected')
    messages.success(request, 'Leave application rejected.')
    return redirect('home')


def update_leave_status(leave_id, status):
    """Helper function to update leave status."""
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = status
    leave.save()


