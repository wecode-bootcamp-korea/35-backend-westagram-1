from django.db import models

class User(models.Model): 
    name         = models.CharField(max_length=20)
    email        = models.CharField(max_length=254, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'