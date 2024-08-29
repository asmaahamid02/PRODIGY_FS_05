from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from typing import Any

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
    

