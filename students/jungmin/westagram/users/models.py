from unittest.util import _MAX_LENGTH
from django.db import models

class User(models.Model):
    name          = models.CharField(max_length=45)
    email         = models.CharField(max_length=200)
    password      = models.CharField(max_length=45)
    mobile_number = models.CharField(max_length=100)
    
    class Meta: 
        db_table = 'users'