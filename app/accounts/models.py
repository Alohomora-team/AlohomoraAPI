from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from condos.models import Apartment, Block

class UserManager(BaseUserManager):
    """A model to manage users"""
    def create_user(self, email, password=None, **kwars):
    """Creates and saves a User with the given email and password"""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves ia superuser with the given email and password."""
        superuser = self.create_user(email, password=password)
        superuser.is_admin = True
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser

class User(AbstractUser):
    """Based on the user model already created for authentication"""
    is_resident = models.BooleanField('student status', default=False)
    is_admin = models.BooleanField('admin status', default=False)
    is_service = models.BooleanField('service status', default=False)
    is_visitor = models.BooleanField('visitor status', default=False)
    is_active = models.BooleanField('active status', default=False)

    username = models.CharField(max_length=40, unique=False, null=True)
    email = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=80)

    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Service(models.Model):
    """A model to store service data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90)
    password = models.CharField(max_length=80)

class Resident(models.Model):
    """A model to store residents data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    complete_name = models.CharField(max_length=80)
    email = models.CharField(max_length=90, unique=True)
    phone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11)
    admin = models.BooleanField(default=False)
    password = models.CharField(max_length=80)

    # TODO() - Colocar null como false nestes 2 campos
    # A mudança deve ser cuidadosa pois existem
    # dependencias, principalmente nos testes
    voice_data = models.TextField(null=True)
    mfcc_audio_speaking_name = models.TextField(null=True)

    #objects = UserManager()

    apartment = models.ForeignKey(Apartment, models.SET_NULL, null=True)
    block = models.ForeignKey(Block, models.SET_NULL, null=True)

    entries = models.ManyToManyField(Apartment, related_name='entries', through='Entry')

class Visitor(models.Model):
    """A model to store visitors data"""
    complete_name = models.CharField(max_length=80)
    cpf = models.CharField(max_length=11, unique=True)

    entries = models.ManyToManyField(Apartment, through='EntryVisitor')

class EntryVisitor(models.Model):
    """A model to store some visitors entry data"""
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    pending = models.BooleanField('entry status', default=True)

class Entry(models.Model):
    """A model to store some residents entry data"""
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

class Admin(models.Model):
    """A model to connect a admin to his creator"""
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admins')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
