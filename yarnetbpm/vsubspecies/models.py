from django.db import models

# Create your models here.
from violation.models import Violation

class VSubspecies(models.Model):
  name = models.CharField(max_length=255)
  violation = models.ForeignKey(Violation, on_delete=models.PROTECT, default=None)

  def __str__(self):
    return f"{self.name}"