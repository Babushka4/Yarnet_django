from django.db import models

# Create your models here.
from company.models import Company
from user.models import User
from regulations.models import Regulations
from decorators.ClassDecorators import with_json_serialize

@with_json_serialize
class Task(models.Model):
  class District(models.TextChoices):
    DZE = 'DZE', 'Дзержинский'
    KIR = 'KIR', 'Кировский'

  name = models.CharField(max_length=255)
  regulations = models.ForeignKey(Regulations, on_delete=models.DO_NOTHING)
  stage = models.ForeignKey(Regulations.Stage, on_delete=models.DO_NOTHING, default=None, null=True)
  author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='task_author')
  performer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='task_performer')
  is_completed = models.BooleanField(default=False)

  @property
  def all_fields(self):
    all_fields = [*list(self.regulations.newfields_set.all())]
    reg_parent = self.regulations.parent

    while reg_parent != None:
      current_reglament_fields = list(reg_parent.newfields_set.all())
      all_fields = [*all_fields, *current_reglament_fields]
      reg_parent = reg_parent.parent
    
    return list(set(all_fields))


  @property
  def table_fields(self):
    return list(filter(lambda x: x.show_in_table == True, self.all_fields))

@with_json_serialize
class Fields(models.Model):
  class Types(models.TextChoices):
    STRING = 'STR', 'СТРОКА'
    INTEGER = 'INT', 'ЦЕЛОЕ ЧИСЛО'
    FLOAT = 'FLT', 'ДРОБНОЕ ЧИСЛО'
    DATE = 'DAT', 'ДАТА'
    FILE = 'FIL', 'ФАЙЛ'
    LIST = 'LIS', 'СПИСОК'
    USER = 'USR', 'СОТРУДНИК'
    COMPANY = 'CMP', 'ОРГАНИЗАЦИЯ'
    DISTRICT = 'DIS', 'РАЙОН'
    NUM = 'NUM', 'НОМЕР'
    
  field_type = models.CharField(max_length=3, choices=Types.choices)
  title = models.CharField(max_length=255)
  show_in_table = models.BooleanField(default=False)
  stage = models.ForeignKey(Regulations.Stage, on_delete=models.DO_NOTHING, default=None, null=True)

  def get_first_value(self):
    try:
      return self.newvalues_set.all()[0].value
    except IndexError:
      return None

@with_json_serialize
class Values(models.Model):
  field = models.ForeignKey(Fields, on_delete=models.DO_NOTHING)
  task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, default=None, null=True)
  value_string = models.CharField(max_length=255, default=None, null=True)
  value_int = models.IntegerField(default=None, null=True)
  value_float = models.FloatField(default=None, null=True)
  value_date = models.DateTimeField(default=None, null=True)
  value_file = models.FileField(default=None, null=True)
  value_list = models.CharField(default=None, null=True, max_length=100)
  value_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, null=True)
  value_company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=None, null=True)
  value_district = models.CharField(max_length=3, default=None, null=True, choices=Task.District.choices)
  is_choosed = models.BooleanField(default=None, null=True)

  @property
  def value(self):
    search_map = {
      Fields.Types.STRING:
        lambda: self.value_string,

      Fields.Types.INTEGER:
        lambda: self.value_int,

      Fields.Types.FLOAT:
        lambda: self.value_float,

      Fields.Types.DATE:
        lambda: self.value_date,

      Fields.Types.FILE:
        lambda: self.value_file,

      Fields.Types.LIST:
        lambda: self.value_list,

      Fields.Types.USER:
        lambda: self.value_user,

      Fields.Types.COMPANY:
        lambda: self.value_company,

      Fields.Types.DISTRICT:
        lambda: self.value_district,

      Fields.Types.NUM:
        lambda: self.value_string,
    }

    try:
      return search_map[self.field.field_type]()
    except KeyError:
      raise TypeError(f'Unknown type "{self.field.field_type}"')

  @value.setter
  def value(self, value):
    def str_set():
      self.value_string = value

    def int_set():
      self.value_int = value

    def float_set():
      self.value_float = value

    def date_set():
      self.value_date = value

    def file_set():
      self.value_file = value

    def list_set():
      self.value_list = value

    def user_set():
      user = User.objects.filter(pk=value)[0]
      self.value_user = user

    def company_set():
      company = Company.objects.filter(pk=value)[0]
      self.value_company = company

    def district_set():
      if value in Task.District.choices:
        self.value_district = value
      else:
        raise ValueError('Incorrect field "district"')

    def number_set():
      self.value_string = value

    def search_map():
      search_map = {
        Fields.Types.STRING: str_set,
        Fields.Types.INTEGER: int_set,
        Fields.Types.FLOAT: float_set,
        Fields.Types.DATE: date_set,
        Fields.Types.FILE: file_set,
        Fields.Types.LIST: list_set,
        Fields.Types.USER: user_set,
        Fields.Types.COMPANY: company_set,
        Fields.Types.DISTRICT: district_set,
        Fields.Types.NUM: number_set,
      }

      search_map[self.field.field_type](value)

    search_map()