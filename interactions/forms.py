from typing import Any
from django import forms
from .models import Comment
from myapp.utils.helper_utils import remove_image_file

class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=500, required=False)    
    image = forms.ImageField(allow_empty_file=True, required=False)
    clear_image = forms.BooleanField(required=False)

    class Meta:
        model = Comment
        fields = [
            'content',
            'image',
            'clear_image'
        ]

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean() 

        if self.is_valid():
            if not cleaned_data.get('content') and not cleaned_data.get('image'):
                raise forms.ValidationError("The post must contain either a content or an image")
            
            if not cleaned_data.get('content') and cleaned_data.get('clear_image'):
                raise forms.ValidationError("The post must contain either a content or an image")
        
        return cleaned_data
    
    
    def save(self, commit: bool = ...) -> Any:
        comment = super(CommentForm, self).save(commit=False)
        old_image = comment.image

        if self.cleaned_data.get('content'):
            comment.content = self.cleaned_data.get('content')
        if self.cleaned_data.get('image') and self.cleaned_data.get('clear_image') == False:
            comment.image = self.cleaned_data.get('image')

        if commit:
            # Remove old images after new ones are successfully saved
            if self.cleaned_data.get('image') and old_image and self.cleaned_data.get('image') != old_image :
                remove_image_file(old_image)
            
            # Remove image if cleared
            if old_image and self.cleaned_data.get('clear_image') == True:
                if comment.image:
                    remove_image_file(old_image)
                    comment.image.delete()

            comment.save()

        return comment

    