from django.db import models

from decorators.ClassDecorators import with_json_serialize

@with_json_serialize
class Company(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.name} [{self.id}]"

  @property
  def displayed_name(self):
    return f"{self.name}"