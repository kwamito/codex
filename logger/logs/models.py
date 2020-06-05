from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image
# Create your models here.

class Profile(models.Model):
    date_joined = models.DateField(default=timezone.now)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg',upload_to='avatars')
    bio = models.CharField(max_length=50)
    
    def __str__(self):
        return self.bio
    def get_absolute_url(self):
        return reverse('profile-detail',kwargs={'pk':self.pk})
    


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField(blank=True)
    title = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True,upload_to='log-images')
    image2 = models.ImageField(blank=True,upload_to='log-images')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('log-detail',kwargs={'pk':self.pk})


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    date_sent = models.DateField(auto_now_add=True)
    reply = models.TextField()
    code = models.TextField(blank=True)

    def __str__(self):
        return self.reply


class Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project_name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    language = models.CharField(max_length=20)

    def __str__(self):
        return self.project_name
    
    def get_absolute_url(self):
        return reverse('project-detail',kwargs={'pk':self.pk})

class Files(models.Model):
    file_n = models.FileField(upload_to='files')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return '{}'.format(self.file_n)

    def get_absolute_url(self):
        return reverse('project-detail',kwargs={'pk':self.project.id})