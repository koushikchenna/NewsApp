from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class hotnews(models.Model):
    title = models.CharField(max_length=20000, null=True)
    source = models.CharField(max_length=20000, null=True)
    author = models.CharField(max_length=20000, null=True)
    description = models.CharField(max_length=20000, null=True)
    content = models.CharField(max_length=200000, null=True)
    lean = models.FloatField(max_length=200000, null=True)
    polar = models.FloatField(max_length=200000, null=True)

class searchnews(models.Model):
    title = models.SlugField(max_length=20000, null=True)
    source = models.SlugField(max_length=20000, null=True)
    author = models.CharField(max_length=20000, null=True)
    description = models.CharField(max_length=20000, null=True)
    content = models.CharField(max_length=200000, null=True)
    urls = models.CharField(max_length=200000, null=True)
    lean = models.FloatField(max_length=200000, null=True)
    polar = models.FloatField(max_length=200000, null=True)

class idnews(models.Model):
    title = models.SlugField(max_length=20000, null=True)
    idtitle = models.IntegerField(blank=True)

class keyword(models.Model):
    username = models.CharField(max_length=20000, null=True)
    keyword = models.CharField(max_length=20000, null=True)

class mynews(models.Model):
    title = models.SlugField(max_length=20000, null=True)
    source = models.SlugField(max_length=20000, null=True)
    author = models.CharField(max_length=20000, null=True)
    description = models.CharField(max_length=20000, null=True)
    content = models.CharField(max_length=200000, null=True)
    urls = models.CharField(max_length=200000, null=True)
    lean = models.FloatField(max_length=200000, null=True)
    polar = models.FloatField(max_length=200000, null=True)
    imgurl = models.CharField(max_length=200000, null=True)

class usersettings(models.Model):
    user = models.CharField(max_length=20000, null=True)
    setting = models.CharField(max_length=20000, null=True)
