from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')

    # # Add any additional attributes you want
    #portfolio_site = models.URLField(blank=True)
    # # pip install pillow to use this!
    # # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    #profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    mob_no = models.CharField(max_length=10,blank=False,default=None)
    college = models.CharField(max_length=120,blank=False,default=None)
    dept = models.CharField(max_length=120,blank=False,default=None)
    college_reg_id = models.CharField(max_length=50,blank=False,default=None)
    food_pref = models.CharField(max_length=10,blank=True,default='ND')
    #Events------------------------------
    pp = models.BooleanField(default=False)
    bat= models.BooleanField(default=False)
    tq = models.BooleanField(default=False)
    ar = models.BooleanField(default=False)
    aio = models.BooleanField(default=False)
    ty = models.BooleanField(default=False)
    syt = models.BooleanField(default=False)
    mod = models.BooleanField(default=False)
    th = models.BooleanField(default=False)
    pubg = models.BooleanField(default=False)
    # tiktok = models.BooleanField(default=False)
    # opm = models.BooleanField(default=False)
    # mc = models.BooleanField(default=False)
    # meme = models.BooleanField(default=False)
    payment_stats = models.BooleanField(default=False)
    cs = models.BooleanField(default=False)
    

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username


class Log(models.Model):
    refuser = models.CharField(max_length=10,blank=False,default=None)
    mob_no_log = models.CharField(max_length=10,blank=False,default=None)
    email_log = models.CharField(max_length=50,blank=False,default=None)
