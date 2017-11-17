from django.db import models

class User(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.TextField()
    
# Create your models here.
