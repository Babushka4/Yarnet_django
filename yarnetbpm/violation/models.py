from django.db import models

# Create your models here.

class Violation(models.Model):
  name = models.CharField(max_length=255)

  def get_subspecies(self):
    return self.vsubspecies_set.all()

  def __str__(self):
      return f"{self.name}"