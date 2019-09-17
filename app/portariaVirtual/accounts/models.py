from django.db import models
from django import forms

# Create your models here.

class User(models.Model):
    
    admin = models.BooleanField(
        default = False,
    )

    complete_name = models.CharField(
        max_length = 80,
    )
    email = models.CharField(
        max_length = 90,
    )

    cpf = models.IntegerField(
        null = True,
    )

    password = models.CharField(
        max_length=50,
    )
    phone = models.CharField(
        max_length = 9,
    )

    voice_data = models.TextField(
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

    cpf = models.IntegerField(
        null = True,
    )

    voice_data = models.TextField(
        null = True,
    )

    phone = models.CharField(
        max_length = 9,
    )
