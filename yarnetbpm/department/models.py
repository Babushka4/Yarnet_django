from django.db import models

from company.models import Company
from decorators.ClassDecorators import with_json_serialize

@with_json_serialize
class Department(models.Model):
  name = models.CharField(max_length=255)
  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, default=None)

  def __str__(self):
        return f"{self.name} [{self.id}]"