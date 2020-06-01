from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)


class Restaurant(models.Model):
    name = models.CharField(max_length=100, blank=False)
    location = models.CharField(max_length=100, blank=False)
    # logo = models.ImageField(upload_to='restaurant_logo')
    info = models.CharField(max_length=100, blank=False)
