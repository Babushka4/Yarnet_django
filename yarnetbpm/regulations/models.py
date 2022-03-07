from django.db import models

from user.models import User
from decorators.ClassDecorators import with_json_serialize

# Create your models here.

@with_json_serialize
class Stage(models.Model):
  class Types(models.TextChoices):
    DEFAULT = 'DEF', 'СТАНДАРТ'
    ERROR = 'ERR', 'ОШИБКА'
    SUCCESS = 'SUC', 'УСПЕХ'
    WAIT = 'WAI', 'ОЖИДАНИЕ'

  scheme = models.CharField(max_length=3, choices=Types.choices, default=Types.DEFAULT)
  title = models.CharField(max_length=100, default=None, null=True)
  button_name = models.CharField(max_length=255, default=None, null=True)
  performer = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, null=True)
  parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, default=None, null=True)

  @property
  def childs(self):
    return self.stage_set.all()

@with_json_serialize
class Regulations(models.Model):
  performer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="reg_performer", default=None, null=True)
  author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="reg_author", default=None, null=True)
  first_stage = models.ForeignKey('Stage', on_delete=models.DO_NOTHING, default=None, null=True)
  name = models.CharField(max_length=255)
  Stage = Stage