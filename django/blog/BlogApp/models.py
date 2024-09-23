from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=25)
    subscription = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_post = models.ImageField(default=None, upload_to='img/')
    
    # Define o campo created_at para ser a data/hora da criação
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Define o campo updated_at para ser atualizado toda vez que o objeto for salvo
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' / ' + str(self.author)
