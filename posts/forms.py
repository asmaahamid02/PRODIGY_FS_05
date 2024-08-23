from typing import Any
from django import forms
from .models import Post
import os, shutil
from myapp.utils.helper_utils import remove_image_file

class PostForm(forms.ModelForm):
    body = forms.CharField(max_length=500, required=False)    
    image = forms.ImageField(allow_empty_file=True, required=False)
    clear_image = forms.BooleanField(required=False)

    class Meta:
        model = Post
        fields = [
            'body',
            'image',
            'clear_image'
        ]

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()    
        if not cleaned_data.get('body') and not cleaned_data.get('image'):
            raise forms.ValidationError("The post must contain either a body or an image")
        
        if not cleaned_data.get('body') and cleaned_data.get('clear_image'):
            raise forms.ValidationError("The post must contain either a body or an image")
        
        return cleaned_data
    
    
    def save(self, commit: bool = ...) -> Any:
        post = super(PostForm, self).save(commit=False)
        old_image = post.image

        if self.cleaned_data.get('body'):
            post.body = self.cleaned_data.get('body')
        if self.cleaned_data.get('image') and self.cleaned_data.get('clear_image') == False:
            post.image = self.cleaned_data.get('image')

        if commit:
            # Remove old images after new ones are successfully saved
            if self.cleaned_data.get('image') and old_image and self.cleaned_data.get('image') != old_image :
                remove_image_file(old_image)
            
            # Remove image if cleared
            if old_image and self.cleaned_data.get('clear_image') == True:
                if post.image:
                    remove_image_file(old_image)
                    post.image.delete()

            post.save()

        return post

    