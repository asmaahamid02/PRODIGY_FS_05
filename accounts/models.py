from django.db import models
from myapp.utils.helper_utils import generate_unique_folder_name
from myapp.utils.image_utils import validate_image_size, resize_image
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from typing import Any

# Create your models here.
class Profile(models.Model):
    def upload_path(self, filename:str) -> str:
        return f"profiles/{self.user.id}/{generate_unique_folder_name()}/{filename}"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')     
    cover_image = models.ImageField(upload_to=upload_path, blank=True, null=True, validators=[validate_image_size])
    profile_image = models.ImageField(upload_to=upload_path, blank=True, null=True, validators=[validate_image_size])
    bio = models.CharField(max_length=1000, blank=True, null=True)
    likes_count = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
    
    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.cover_image:
            new_image = resize_image(self.cover_image, (900,))
            self.cover_image = new_image
        if self.profile_image:
            new_image = resize_image(self.profile_image, (150,))
            self.profile_image = new_image    
        return super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def _create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)