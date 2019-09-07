from django.db import models
from django import forms

# Create your models here.

class User(models.Model):

    complete_name = models.CharField(
        max_length = 80,
    )
    email = models.CharField(
        max_length = 90,
    )
    password = models.CharField(
        max_length=50,
    )
    phone = models.CharField(
        max_length = 9,
    )
    apartment = models.IntegerField(
        blank = True,
        null = True,
    )
    block = models.CharField(
        max_length = 6,
        blank = True,
        null = True,
    )

class Visitor(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    complete_name = models.CharField(
        max_length = 80,
    )
    email = models.CharField(
        max_length = 90,
    )
    phone = models.CharField(
        max_length = 9,
    )
