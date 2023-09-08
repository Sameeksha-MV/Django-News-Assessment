from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, User

class CustomUser(AbstractUser):
  is_author = models.BooleanField(default=False)
  is_publisher = models.BooleanField(default=False)

class Article(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    description = models.TextField()
    author = models.ForeignKey(CustomUser, related_name="authored_articles", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Draft')  # Draft, Review, Published

     