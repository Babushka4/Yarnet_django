from django.db import models

from decorators.ClassDecorators import with_json_serialize

@with_json_serialize
class Organization(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
      return f"{self.name} [{self.id}]"