from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Follower(models.Model):
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.followed_by.username} follows {self.following.username}"
    
    class Meta:
        unique_together = ('followed_by', 'following')
    