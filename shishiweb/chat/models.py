from django.db import models

class User(models.Model):
    login = models.TextField()
    password = models.TextField()
    name = models.TextField()
    surname = models.TextField()
    bot_mark = models.TextField()