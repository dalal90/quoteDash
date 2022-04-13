from django.db import models

import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+$')

        if len(postData['fname']) < 2:
            errors['fname'] = "first names must be more than 2 characters.Only CHARACTERS "
        if len(postData['lname']) < 2:
            errors['lname'] = "last names must be more than 2 characters.Only CHARACTERS  "
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid e-mail address!"
        if len(postData['password']) < 8:
            errors['password'] = "Passwords must be 8+ characters"
        if postData['password']!=postData['confirm_password']:
            errors['password']="Password must be match!!"
        return errors
    
    def update_validator(self, postData):
        errors = {}
        user_in_db = User.objects.filter(email=postData['Email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+$')

        if len(postData['f_name']) < 2:
            errors['f_name'] = "first names must be more than 2 characters.Only CHARACTERS "
        if len(postData['l_name']) < 2:
            errors['l_name'] = "last names must be more than 2 characters.Only CHARACTERS  "
        if not EMAIL_REGEX.match(postData['Email']):
            errors['Email'] = "Invalid e-mail address!"
        if user_in_db:
            errors['Email'] = "User already exists"
        return errors

    def login_validator(self, postData ):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            login_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), login_user.password.encode()):
                errors['password'] = "Invalid login"
        else:
            errors['password'] = "Invalid login"
        return errors 
    
    def quote_validator(self, postData):
        errors = {}
        if len(postData['Author']) < 3:
            errors['Author'] = "Author names must be at least 3 charecters "
        if len(postData['quote']) < 10:
            errors['quote'] = "quote must be at more than 10 charecters "
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=30)
    # Time/Date Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    Author= models.CharField(max_length=255)
    quote = models.TextField()
    poster= models.ForeignKey(User, related_name="poster", on_delete = models.CASCADE)
    like = models.ManyToManyField(User, related_name="like")
    # Time/Date Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)