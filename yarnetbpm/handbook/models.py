from django.db import models
from user.models import User
from decorators.ClassDecorators import with_json_serialize


class HandBookCategory(models.Model):
    """Категория справочника справочников
    Каждой категории привязан перечень полей, актуальных для неё (HandBookField)
    и объекты справочника с определенной иерархией из HandBookObjects."""
    title = models.CharField(max_length=100, default=None, null=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, null=True)
    creation_date = models.DateField(auto_now=True)
    # одно поле может быть привязяно ко множеству категорий, а у категории
    # может быть множество полей
    fields = models.ManyToManyField('HandBookField', blank=True)


@with_json_serialize
class HandBookObject(models.Model):
    """Иерархия объектов справочника, к которым в таблице значений (HandBookValues)
        соответствует перечень значений по определенным полям."""
    category = models.ForeignKey(HandBookCategory, on_delete=models.DO_NOTHING, default=None, null=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, default=None, null=True)


@with_json_serialize
class HandBookField(models.Model):
    """Перечень полей, связанный с категориями, в которых данный тип поля должен быть."""

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
    title = models.CharField(max_length=25, null=True)
    # category = models.ManyToManyField(HandBookCategory, blank=True)



@with_json_serialize
class HandBookValues(models.Model):
    """Значения для полей из HandBookField
    каждое значение соответствует определенному объекту справочникак (HandBookObject)."""
    field = models.ForeignKey(HandBookField, on_delete=models.DO_NOTHING, default=None)
    hb_object = models.ForeignKey(HandBookObject, on_delete=models.DO_NOTHING, default=None)
    value_string = models.CharField(max_length=255, default=None, null=True)
    value_int = models.IntegerField(default=None, null=True)
    value_float = models.FloatField(default=None, null=True)
    value_date = models.DateTimeField(default=None, null=True)
    value_file = models.FileField(default=None, null=True)
    value_list = models.CharField(default=None, null=True, max_length=100)

    def __init__(self, *args, value=None, field=None, **kwargs):
        """Исходя из типа поля определяется в какой столбец таблицы поместить значение."""

        search_map = {
            HandBookField.Types.STRING: 'value_string',
            HandBookField.Types.INTEGER: 'value_int',
            HandBookField.Types.FLOAT: 'value_float',
            HandBookField.Types.DATE: 'value_date',
            HandBookField.Types.FILE: 'value_file',
            HandBookField.Types.LIST: 'value_list',
            HandBookField.Types.NUM: 'value_string',
        }

        try:
            if (value != None):

                if (field.field_type == HandBookField.Types.NUM):
                    kwargs[search_map[field.field_type]] = f'№ {value}'

                else:
                    kwargs[search_map[field.field_type]] = value

            if (field != None):
                kwargs['field'] = field

            super().__init__(*args, **kwargs)
        except KeyError:
            raise TypeError(f'Unknown type "{field.field_type}"')