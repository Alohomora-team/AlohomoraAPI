from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from condos.models import Apartment, Block

class ServiceManager(BaseUserManager):
    def create_service(self, email, password=None, **kwars):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        service = self.model(
            email=self.normalize_email(email),
        )

        service.set_password(password)
        service.save(using=self._db)
        return service

class Service(AbstractUser):
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=40, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class User(models.Model):
    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90, unique=True)
    phone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11)
    admin = models.BooleanField(default=False)
    voice_data = models.TextField(null=True)
    #objects = UserManager()

    apartment = models.ForeignKey(Apartment, models.SET_NULL, null=True)
    block = models.ForeignKey(Block, models.SET_NULL, null=True)


class Visitor(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11)
    voice_data = models.TextField(null=True)
