from django.db import models

# Create your models here.

class User(models.Model):
    name          = models.CharField(max_length=50)
    email         = models.CharField(max_length=100, unique=True)
    password      = models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'