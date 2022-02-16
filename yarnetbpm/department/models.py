from django.db import models

from organization.models import Organization
from decorators.ClassDecorators import with_json_serialize

@with_json_serialize
class Department(models.Model):
  name = models.CharField(max_length=255)
  organizations = models.ManyToManyField(Organization)

  def __str__(self):
        return f"{self.name} [{self.id}]"