from django import forms
from django.contrib.auth.models import User
from account.models import UserProfile

class UserProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True, label="Name")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = UserProfile
        fields = ['position', 'place']

    def save(self, commit=True):
        # Save the user profile first
        user_profile = super().save(commit=False)
        
        # Get the related user object and update their details
        user = self.instance.user
        user.username = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            user_profile.save()
        return user_profile
