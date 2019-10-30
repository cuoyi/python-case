from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=18)


class EBook(models.Model):
    bookname = models.CharField(max_length=30)
    bookauthor = models.CharField(max_length=30)
    bookurl = models.CharField(max_length=100)