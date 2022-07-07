from django.db import models

class User(models.Model): 
    name         = models.CharField(max_length=20)
    email        = models.CharField(max_length=254)
    password     = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    class Meta: 
        db_table = 'users'