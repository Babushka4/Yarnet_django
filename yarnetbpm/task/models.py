from datetime import datetime
from django.db import models

# Create your models here.
from company.models import Company
from user.models import User
from regulations.models import Regulations
from decorators.ClassDecorators import with_json_serialize
# from handbook.models import HandBookCategory


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


  # возвращает из БД поля в хронолгическом порядке
  @property
  def all_fields(self):
    all_fields = [*list(self.stage.fields_set.all())]
    stage_parent = self.stage.parent

    while stage_parent != None:
      current_reglament_fields = list(stage_parent.fields_set.all())
      all_fields = [*all_fields, *current_reglament_fields]
      stage_parent = stage_parent.parent

    return list(set(all_fields))

  # возвращает набор полей со значением True св-ва show_in_table
  @property
  def table_fields(self):
    return list(filter(lambda x: x.show_in_table, self.all_fields))

  # получение всех значений полей
  @property
  def all_values(self):
    return self.values_set.all()

  # возвращает все связанные с таблицой поля и их значения
  @property
  def table_values(self):
    table_fields = self.table_fields
    all_values = self.all_values

    return list(filter(lambda value: value.field in table_fields, all_values))
  

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
    NUM = 'NUM', 'НОМЕР',
    # доюавление справочника к типам полей этапа
    HB = 'HB', 'СПРАВОЧНИК'
    
  field_type = models.CharField(max_length=3, choices=Types.choices)
  title = models.CharField(max_length=255)
  show_in_table = models.BooleanField(default=False)
  stage = models.ForeignKey(Regulations.Stage, on_delete=models.DO_NOTHING, default=None, null=True)

  def get_first_value(self):
    try:
      value = self.values_set.filter()[0].value

      if isinstance(value, models.Model):
        return value.displayed_name

      return value
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
  # поле, ссылающееся на справочник по его id
  # value_handbook = models.ForeignKey(HandBookCategory, on_delete=models.DO_NOTHING, default=None, null=True)

  def __init__(self, *args, value=None, field=None, **kwargs):

    search_map = {
      Fields.Types.STRING: 'value_string',
      Fields.Types.INTEGER: 'value_int',
      Fields.Types.FLOAT: 'value_float',
      Fields.Types.DATE: 'value_date',
      Fields.Types.FILE: 'value_file',
      Fields.Types.LIST: 'value_list',
      Fields.Types.USER: 'value_user',
      Fields.Types.COMPANY: 'value_company',
      Fields.Types.DISTRICT: 'value_district',
      Fields.Types.NUM: 'value_string',
      Fields.Types.HB: 'value_handbook'
    }

    try:
      if (value != None):

        if (field.field_type == Fields.Types.NUM):
          kwargs[search_map[field.field_type]] = f'№ {value}'

        else:
          kwargs[search_map[field.field_type]] = value

      if (field != None):
        kwargs['field'] = field

      super().__init__(*args, **kwargs)
    except KeyError:
      raise TypeError(f'Unknown type "{field.field_type}"')

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
      [user] = User.objects.filter(pk=value)
      self.value_user = user

    def company_set():
      [company] = Company.objects.filter(pk=value)
      self.value_company = company

    def district_set():
      self.value_district = value

    def number_set():
      self.value_string = f'№ {value}'

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

    try:
      search_map()
    except KeyError:
      raise TypeError(f'Unknown type "{self.field.field_type}"')

  def displayed_value(self):
    value = self.value

    if isinstance(value, models.Model):
      return value.displayed_name

    return value

class HistoryManager(models.Manager):
  def new_record(self, task, stage, action, author, date=None):
    date = date if date != None else datetime.now()
    rec = self.model(
      task=task,
      stage=stage,
      action=f"{action}; Автор: {author.fullname}.",
      author=author,
      datetime=date,
    )
    rec.save()
    
    return rec
  
  def group_by_date(self, task):
    result = { }

    for record in self.model.objects.filter(task=task).order_by('datetime'):
        str_date = record.datetime.strftime('%d.%m.%y')

        if str_date not in result:
          result[str_date] = []

        result[str_date].append(record)

    return result


class History(models.Model):
  task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, null=True, default=None)
  stage = models.ForeignKey(Regulations.Stage, on_delete=models.DO_NOTHING, null=True, default=None)
  datetime = models.DateTimeField()
  action = models.CharField(max_length=65535)
  author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

  objects = HistoryManager()

  _previous = None

  def __str__(self):
    return f"{self.datetime.strftime('%d.%m.%y %H:%M')} {self.action}"

  @property
  def previous(self):
    return History._previous

  def set_previous(self):
    History._previous = self


