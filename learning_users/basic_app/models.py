from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # Add any additional attributes you want
    portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

class userInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    f_name=models.CharField(max_length=20)
    l_name=models.CharField(max_length=20)
    email=models.EmailField(max_length=70,primary_key=True)
    mob=models.PositiveIntegerField
    active=models.BooleanField(default=False)
    password=forms.CharField(widget=forms.PasswordInput())

    #Address

    house=models.CharField(max_length=40)
    street=models.CharField(max_length=185)
    dist=models.CharField(max_length=185)
    state=models.CharField(max_length=185)
    pin=models.PositiveIntegerField

class ms_code_updater(models.Model):
    intcode=models.PositiveIntegerField(default=1112)

