from django import forms
from django.contrib.auth.models import User
from typing import Any
import os, shutil
from myapp.utils.helper_utils import remove_image_file

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
            # Remove old images after new ones are successfully saved
            if self.cleaned_data.get('profile_image') and old_profile_image:
                remove_image_file(old_profile_image)

            if self.cleaned_data.get('cover_image') and old_cover_image:
                remove_image_file(old_cover_image)
            
            user.save()
            user.profile.save() 
        return user

    