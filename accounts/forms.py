from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from typing import Any
import os, shutil

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if email:
            found = User.objects.filter(email=email).exists()

            if found:
                self.add_error('email', forms.ValidationError('This email is used before.'))
        return cleaned_data
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']    

    bio = forms.CharField(required=False)
    profile_image = forms.ImageField(required=False)
    cover_image = forms.ImageField(required=False)    

    def save(self, commit: bool = ...) -> Any:
        user = super(UserProfileForm, self).save(commit=False)

        old_profile_image = user.profile.profile_image
        old_cover_image = user.profile.cover_image
        
        if self.cleaned_data.get('profile_image'):
            user.profile.profile_image = self.cleaned_data.get('profile_image')
        if self.cleaned_data.get('cover_image'):
            user.profile.cover_image = self.cleaned_data.get('cover_image')
        if self.cleaned_data.get('bio'):
            user.profile.bio = self.cleaned_data.get('bio')

        if commit:
            user.save()
            user.profile.save()      
            
            # Remove old images after new ones are successfully saved
            if self.cleaned_data.get('profile_image') and old_profile_image:
                if hasattr(old_profile_image, 'path') and os.path.exists(old_profile_image.path):
                    dir = old_profile_image.path.rsplit('/', 1)[0]
                    if os.path.exists(dir) and os.path.isdir(dir):
                        shutil.rmtree(dir)

            if self.cleaned_data.get('cover_image') and old_cover_image:
                if hasattr(old_cover_image, 'path') and os.path.exists(old_cover_image.path):
                    dir = old_cover_image.path.rsplit('/', 1)[0]
                    if os.path.exists(dir) and os.path.isdir(dir):
                        shutil.rmtree(dir)
            
        return user

    