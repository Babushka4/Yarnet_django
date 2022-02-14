from django.db import models

from department.models import Department

class Employee(models.Model):
    fullname = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    position = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
