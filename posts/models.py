from django.db import models
from django.contrib.auth.models import User
from typing import Any
from myapp.utils import image_utils
from myapp.utils.helper_utils import generate_unique_folder_name
from django.dispatch import receiver
from django.db.models.signals import post_delete
from myapp.utils.signal_utils import file_cleanup
import os, shutil

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

    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]:
        post = super().delete(*args, **kwargs)    

        if self.image:
            print(self.image)

            if hasattr(self.image , 'path') and os.path.exists(self.image.path):
                print(self.image.path)

                dir = self.image.path.rsplit('/', 1)[0]

                if os.path.exists(dir) and os.path.isdir(dir):
                    shutil.rmtree(dir)

        return post
    
# @receiver(post_delete, sender=Post)
# def _delete_post_image(sender, instance, **kwargs):
#     file_cleanup(instance, 'image')