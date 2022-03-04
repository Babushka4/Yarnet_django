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

  company = models.ForeignKey(Company, on_delete=models.PROTECT)
  district = models.CharField(max_length=100, choices=District.choices)
  date = models.DateTimeField()
  number = models.CharField(max_length=6)
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  regulation = models.ForeignKey(Regulations, on_delete=models.PROTECT)

  def __str__(self):
    f""

@with_json_serialize
class NewRegulations(models.Model):
  class Types(models.TextChoices):
    DEFAULT = 'DEF', 'СТАНДАРТ'
    ERROR = 'ERR', 'ОШИБКА'
    SUCCESS = 'SUC', 'УСПЕХ'
    WAIT = 'WAI', 'ОЖИДАНИЕ'

  reg_type = models.CharField(max_length=3, choices=Types.choices, default=Types.DEFAULT)
  title = models.CharField(max_length=100, default=None, null=True)
  button_name = models.CharField(max_length=255)
  performer = models.ForeignKey(User, on_delete=models.PROTECT, default=None, null=True)
  parent = models.ForeignKey('self', on_delete=models.PROTECT, default=None, null=True)

@with_json_serialize
class NewTask(models.Model):
  name = models.CharField(max_length=255)
  regulations = models.ForeignKey(NewRegulations, on_delete=models.PROTECT)
  author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author')
  performer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='performer')

  def get_fields_in_table(self):
    return self.regulations.newfields_set.filter(show_in_table=True)

@with_json_serialize
class NewFields(models.Model):
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
    
  field_type = models.CharField(max_length=3, choices=Types.choices)
  title = models.CharField(max_length=255)
  show_in_table = models.BooleanField(default=False)
  regulations = models.ForeignKey(NewRegulations, on_delete=models.PROTECT, default=None, null=True)

  def get_first_value(self):
    return self.values_set.all()[0].value

@with_json_serialize
class NewValues(models.Model):
  field = models.ForeignKey(NewFields, on_delete=models.PROTECT)
  value_string = models.CharField(max_length=255, default=None, null=True)
  value_int = models.IntegerField(default=None, null=True)
  value_float = models.FloatField(default=None, null=True)
  value_date = models.DateTimeField(default=None, null=True)
  value_file = models.FileField(default=None, null=True)
  value_list = models.CharField(default=None, null=True, max_length=100)
  value_user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, null=True)
  value_company = models.ForeignKey(Company, on_delete=models.PROTECT, default=None, null=True)
  value_district = models.CharField(max_length=3, default=None, null=True, choices=Task.District.choices)
  is_choosed = models.BooleanField(default=None, null=True)

  @property
  def value(self):
    search_map = {
      NewFields.Types.STRING:
        lambda: self.value_string,

      NewFields.Types.INTEGER:
        lambda: self.value_int,

      NewFields.Types.FLOAT:
        lambda: self.value_float,

      NewFields.Types.DATE:
        lambda: self.value_date,

      NewFields.Types.FILE:
        lambda: self.value_file,

      NewFields.Types.LIST:
        lambda: self.value_list,

      NewFields.Types.USER:
        lambda: self.value_user,

      NewFields.Types.COMPANY:
        lambda: self.value_company,

      NewFields.Types.DISTRICT:
        lambda: self.value_district,
    }

    try:
      return search_map[self.field.field_type]()
    except KeyError:
      raise TypeError(f'Unknown type "{self.field.field_type}')

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

    def search_map():
      search_map = {
        NewFields.Types.STRING: str_set,
        NewFields.Types.INTEGER: int_set,
        NewFields.Types.FLOAT: float_set,
        NewFields.Types.DATE: date_set,
        NewFields.Types.FILE: file_set,
        NewFields.Types.LIST: list_set,
        NewFields.Types.USER: user_set,
        NewFields.Types.COMPANY: company_set,
        NewFields.Types.DISTRICT: district_set,
      }

      search_map[self.field.field_type](value)

    search_map()