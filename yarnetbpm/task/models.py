from django.db import models

# Create your models here.
from organization.models import Organization
from district.models import District
from violation.models import Violation
from employees.models import Employee
from status.models import Status


class Task(models.Model):
  organization = models.OneToOneField(Organization, on_delete=models.PROTECT)
  district = models.OneToOneField(District, on_delete=models.PROTECT)
  violation = models.ForeignKey(Violation, on_delete=models.PROTECT)
  date = models.DateTimeField()
  number = models.IntegerField()
  employee = models.OneToOneField(Employee, on_delete=models.PROTECT)
  status = models.OneToOneField(Status, on_delete=models.PROTECT)