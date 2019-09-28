from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

from condos.models import Apartment, Block

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwars):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90, unique=True)
    phone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11)
    admin = models.BooleanField(default=False)
    voice_data = models.TextField(null=True)
    objects = UserManager()

    apartment = models.ForeignKey(Apartment, models.SET_NULL, null=True)
    block = models.ForeignKey(Block, models.SET_NULL, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Visitor(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11)
    voice_data = models.TextField(null=True)
