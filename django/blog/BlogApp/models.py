from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')  # Impede duplicatas

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
    
class Post(models.Model):
    title = models.CharField(max_length=25)
    subscription = models.CharField(max_length=100)
    photo_post = models.ImageField(default=None, upload_to='img/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    def __str__(self):
        return f"{self.title} / {self.author}"

    def clean(self):
        if len(self.title) > 25:
            raise ValidationError('O título não pode ter mais de 25 caracteres.')
        if len(self.subscription) > 100:
            raise ValidationError('A descrição não pode ter mais de 100 caracteres.')

    def is_liked_by(self, user):
        return user in self.likes.all()

    def likes_count(self):
        return self.likes.count()
