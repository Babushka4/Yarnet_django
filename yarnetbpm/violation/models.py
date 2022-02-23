from django.db import models

# Create your models here.
from vsubspecies.models import VSubspecies

class Violation(models.Model):
  name = models.CharField(max_length=255)
  subspecies = models.ForeignKey(VSubspecies, on_delete=models.PROTECT, default=None)

  def __str__(self):
      return f"{self.name}"