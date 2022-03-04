from django.db import models

# Create your models here.

class Regulations(models.Model):
  parent = models.ForeignKey('self', on_delete=models.PROTECT, default=None, null=True)
  status = models.CharField(max_length=255, default='Новая')
  button = models.CharField(max_length=255, default=None, null=True)

  def get_next(self):
    return Regulations.objects.filter(parent=self.id)
