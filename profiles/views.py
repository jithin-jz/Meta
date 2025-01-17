from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import UserProfile
from django.contrib.auth.models import User
from home.forms import UserProfileForm

@login_required
def profile(request):
    # Get or create a user profile for the logged-in user
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    # Pass employee_id to the template
    employee_id = user_profile.employee_id  

    return render(request, 'profile.html', {
        'form': form,
        'user_profile': user_profile,
        'employee_id': employee_id,  
    })


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    
    # Include employee_id in the context
    employee_id = user_profile.employee_id  

    return render(request, 'profile_view.html', {
        'user_profile': user_profile,
        'employee_id': employee_id,  
    })
