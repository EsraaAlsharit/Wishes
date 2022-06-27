from django.db import models
from datetime import datetime
import re
import bcrypt


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        emails = User.objects.filter(email=postData['email'])
        if len(emails) > 0:
            errors['emailExist'] = "This Email is already in use!"
            return errors
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['fname']) < 2:
            errors["fname"] = "first name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "last name should be at least 3 characters"
        if len(postData['pass']) < 8:
            errors["pass"] = "password should be at least 8 characters"
        if (postData['pass'] != postData['cpass']):
            errors['cpass'] = "password is not equal to the confirm password"
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if len(user) == 0:
            errors['none'] = "Email or Password is not correct"

        elif (user[0].email != postData['email']):
            errors['notfound'] = "Email or Password is not correct"

        elif not bcrypt.checkpw(postData['pass'].encode(), user[0].password.encode()):
            errors['passlog'] = "Email or Password is not correct"
        return errors


class User(models.Model):
    fname = models.TextField()
    lname = models.TextField()
    email = models.EmailField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class WishManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors["item"] = "A wish must consist of at least 3 characters!"
        if len(postData['desc']) < 3:
            errors["desc"] = "A Destination must be provided!"
        return errors


class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.TextField()
    isGranted = models.BooleanField()
    grand_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, related_name="wish",
                             on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="likes")
    date_add = models.DateField(auto_now_add=True)
    objects = WishManager()

    def Count(self, request):
        count = self.queryset.count()
        return Response({'count': count})
