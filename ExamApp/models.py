from math import fabs
import re
from django.db import models
import bcrypt
from .models import *


# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if users.objects.filter(email=postData['email']):
            errors['email'] = "Email already exist."
        if len(postData['fname'])<2:
            errors['fname']="First Name should be at least 2 charachters!"
        if len(postData['lname'])<2:
            errors['lname']="Last Name should be at least 2 charachters!"
        if len(postData['password'])<8:
            errors['password8']="Password should be at least 8 charachters!"
        if postData['password']!=postData['cpass']:
            errors['password']="Passwords don't match"
        return errors


    def login_validator(self,postData):
        errors={}
        user = users.objects.filter(email=postData['email'])
        if len(postData['email']) < 8:
            errors['email'] = "Email should be at least 8 characters."
        elif not user:
            errors['email'] = "Username is not found."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors['password'] = "Incorrect password!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."
        return errors

    def wishValid(self,postData):
        errors={}
        if len(postData['item'])<3:
            errors['item']="A item should be at least 3 characters!"
        if len(postData['desc'])<3:
            errors['desc']="Description must be provided."
        return errors

class users(models.Model):
    fname=models.CharField(max_length=45)
    lname=models.CharField(max_length=45)
    email=models.CharField(max_length=45)
    password=models.CharField(max_length=45)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects= UserManager()


class wishs(models.Model):
    user = models.ForeignKey(users,related_name='user',on_delete=models.CASCADE)
    liked_by=models.ManyToManyField(users,related_name='liked_wish')
    item=models.CharField(max_length=255)
    desc=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    granted = models.BooleanField(default=False)
    granted_at = models.DateTimeField(auto_now=True)
    objects= UserManager()

