from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    names = models.CharField(max_length=50)

    def __str__(self):
        return self.names


class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    text = models.TextField()
    tag = models.ForeignKey(Tag)
    category = models.ForeignKey(Category, blank=True, null=True)
    click = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()
 
    def __str__(self):
        return self.title



