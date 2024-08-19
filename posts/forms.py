from typing import Any
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    body = forms.CharField(max_length=500, required=False)    
    image = forms.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = Post
        fields = [
            'body',
            'image',
        ]

    def clean(self) -> dict[str, Any]:

        cleaned_data = super().clean()    
        if not cleaned_data.get('body') and not cleaned_data.get('image'):
            raise forms.ValidationError("The post must contain either a body or an image")
        
        return cleaned_data