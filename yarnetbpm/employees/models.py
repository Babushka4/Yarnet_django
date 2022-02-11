from django.db import models

class Employee(models.Model):
    fullname = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)


