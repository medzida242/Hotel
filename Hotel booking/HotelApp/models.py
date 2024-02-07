from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
from django.utils.crypto import get_random_string
from datetime import timedelta
#from django.contrib.auth.models import User
from django.conf import settings


class Manager(BaseUserManager):

    def create_superuser(self, email, username, password, name, surname, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, username, password, name, surname, **other_fields)

    def create_user(self, email, username, password, name, surname, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, name=name, surname=surname, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=250)
    email = models.EmailField(max_length=80, unique=True)

    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    phone = models.CharField(max_length=15, blank=True)
    cardnum=models.CharField(max_length=16, blank=True, null=True )   
    
    date_of_birth = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = Manager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'name', 'surname']

    def __str__(self):
        return self.username



class Mjesto(models.Model):
    imemjesta=models.CharField(max_length=35)
    drzava=models.CharField(max_length=20)
    
    def __str__(self):
        return self.imemjesta


class Hotel(models.Model):
    ime= models.CharField(max_length=50)
    zvjezdice=models.IntegerField(default=0)
    mjesto= models.ForeignKey(Mjesto, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='hotel_pictures', null=True, blank=True)

    def __str__(self):
        return self.ime
    
class Comment(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.hotel.ime}"

