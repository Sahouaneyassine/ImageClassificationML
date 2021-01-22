from django.db import models

# Create your models here.

class Input(models.Model):
    fullname=models.CharField(max_length=30)
    email=models.EmailField(max_length=254)
    photo = models.ImageField(upload_to='photos/')

