# YarNet BPM

## Installation

1. Clone repo
2. Init and activate environment in root directory

```bash
source yarbpm
```

This command will create virtual environment and initialize it

3. Synchronize all dependencies

```bash
depsync
```

## Usage

Basic comands:

1. `close` - complete work with YarBPM
2. `runserver` - run Django server on host 0.0.0.0:8000
3. `makemigrations` - makes Django migrations
4. `migrate` - Django migrate
5. `createapp {name}` - creates Django application with `name`
6. `addtoapi {version} {method} {action}` - add to api with `version` new `action` with `method`
7. `runscript {path_to_script}` - execute python script
8. `runshell [--standard]` - run djang-shell or python-shell (if the argument was specified)

## Code Documentation

### Decorators

#### JSON serializing

If you'll want to use your model in API in future, you should add `@with_json_serialize` decorator
And next you can use property `as_json` to get json serialized model

**Example**
```python
from django.db import models

from decorators.ClassDecoarators import with_json_serialize

@with_json_serialize
class MyModel(models.Model):
  field1 = model.CharField(max_length=100)
  field2 = model.IntegerField(default=None, null=True)

# ...
```

**Usage**

```python
new_model = MyModel(field1="Some value", field2=3)

new_model.save()
print(MyModel.objects.all()[0].as_json)
# [{"model": "<app>.MyModel", pk=1, "fields": {"field1": "Some value", "field2": 3}}]
```

Also you can serialize QuerySet with built-in property `as_json`

**Usage**

```python
# From pervious example
print(MyModel.object.all().as_json)
# [{"model": "<app>.MyModel", pk=1, "fields": {"field1": "Some value", "field2": 3}}]
```

## API Documentation

### GET requests

`GET /api/v1/employees/` - returns all employees
`GET /api/v1/departments/` - return all departments
`GET /api/v1/companies/` - return all organizations

### POST requests

`POST /api/v1/employees/add/` - add new employee

  **Parameters**
  - `fullname: string` - fullname of employee (length <= 255)
  - `department: int` - department's id of employee
  - `position: string` - position of employee (length <= 100)
  - `email: string` - email of employee (length <= 255)
  - `telephone: string` - employee's telephone number (length <= 255)

`POST /api/v1/departments/add/` - return all departments

  **Parameters**
  - `name: string` - department's name (length <= 255)
  - `organizations: int[]` - organization's ids

`POST /api/v1/organizations/add/` - return all organizations

  **Parameters**
  - `name: string` - organization's name (length <= 255)