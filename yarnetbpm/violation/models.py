from django.db import models

# Create your models here.
from vsubspecies.models import VSubspecies

class Violation(models.Model):
  name = models.CharField(max_length=255)
  subtype = models.ForeignKey(VSubspecies, on_delete=models.PROTECT)