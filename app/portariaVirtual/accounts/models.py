from django.db import models


class User(models.Model):

    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=9)
    password = models.CharField(max_length=50)

    cpf = models.IntegerField(null=True)

    admin = models.BooleanField(default=False)

    voice_data = models.TextField(null=True)



class Visitor(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=9)

    cpf = models.IntegerField(null=True)

    voice_data = models.TextField(null=True)
