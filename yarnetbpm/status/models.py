from django.db import models

# Create your models here.

class Status(models.Model):
  title = models.CharField(max_length=100)

  def __str__(self):
      return f"{self.title} - [{self.id}]"