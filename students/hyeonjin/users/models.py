from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=45)
    email        = models.CharField(max_length=45, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=45)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    # others       = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'users'