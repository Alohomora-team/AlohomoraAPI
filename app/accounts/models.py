from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from condos.models import Apartment, Block

class MyUserManager(BaseUserManager):
    """Creates and saves a Service with the given email and password"""
    def create_service(self, email, password=None, **kwars):
        if not email:
            raise ValueError('Users must have an email address')

        service = self.model(
            email=self.normalize_email(email),
        )

        service.set_password(password)
        service.save(using=self._db)
        return service

    def create_superuser(self, username, password):
        """Creates and saves a superuser with the given email and password."""
        u = self.create_user(username, password=password)
        u.is_admin = True
        u.save(using=self._db)
        return u

class User(AbstractUser):
    """Based on the user model already created for authentication"""
    is_resident = models.BooleanField('student status', default=False)
    is_admin = models.BooleanField('admin status', default=False)
    is_service = models.BooleanField('service status', default=False)
    is_visitor = models.BooleanField('visitor status', default=False)

    username = models.CharField(max_length=40, unique=False)
    email = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=80)

    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Service(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90)
    password = models.CharField(max_length=80)

class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90, unique=True)
    phone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11)
    admin = models.BooleanField(default=False)
    voice_data = models.TextField(null=True)
    password = models.CharField(max_length=80)

    #objects = UserManager()

    apartment = models.ForeignKey(Apartment, models.SET_NULL, null=True)
    block = models.ForeignKey(Block, models.SET_NULL, null=True)

class Visitor(models.Model):
    owner = models.ForeignKey(Resident, on_delete=models.CASCADE, null=True)
    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11)
    voice_data = models.TextField(null=True)
