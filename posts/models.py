from django.db import models
from django.contrib.auth.models import User
from typing import Any
from myapp.utils import image_utils
from myapp.utils.helper_utils import generate_unique_folder_name

class Post(models.Model):
    def image_upload(self, filename):
        return f"posts/{self.author.id}/{generate_unique_folder_name()}/{filename}"
        
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    body = models.CharField(max_length=500)
    image = models.ImageField(upload_to=image_upload, blank=True, null=True, validators=[image_utils.validate_image_size])
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.author.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.image:
            new_image = image_utils.resize_image(self.image)

            if type(new_image) is dict and new_image.get('status') == 'fail':
                raise ValueError(new_image.get('message'))

            self.image = new_image

        super().save(*args, **kwargs)