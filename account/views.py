from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
import pytz

def login(request):
    return render(request, 'login.html')


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

