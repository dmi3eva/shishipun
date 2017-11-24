from django.db import models

class User(models.Model):
    login = models.TextField()
    password = models.TextField()

class Message(models.Model):
    user_id = models.ForeignKey(User)
    text = models.TextField()

class Bot(models.Model):
    user_id = models.ForeignKey(User)
    param1 = models.TextField()