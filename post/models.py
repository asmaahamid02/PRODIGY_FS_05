from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
import uuid
from typing import Any
from datetime import datetime
from myapp.utils import image_utils
import os

class Post(models.Model):
    def image_upload(self, filename):
        #generate a unique folder name
        unique_folder = uuid.uuid4().hex[:6].upper() + '_' + datetime.now().strftime('%Y%m%d%H%M%S')
        return f"posts/{self.author.id}/{unique_folder}/{filename}"
        
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
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