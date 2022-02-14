from django.db import models

class Department(models.Model):
  name = models.CharField(max_length=255)
  organization = models.CharField(max_length=255)