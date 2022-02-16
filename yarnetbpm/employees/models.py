from django.db import models

from department.models import Department
from decorators.ClassDecorators import with_json_serialize

@with_json_serialize
class Employee(models.Model):
    fullname = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    position = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.email} - {self.fullname} [{self.position} -> {self.department}] ({self.id})"

    def get_department_name(self):
        return Department.objects.filter(pk=self.department_id)[0].name
