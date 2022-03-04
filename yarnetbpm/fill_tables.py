from department.models import Department
from user.models import User
from company.models import Company
from task.models import Task, DISTRICT_CHOICES
from violation.models import Violation
from random import randint
from datetime import datetime
from regulations.models import Regulations

MODELS_LIST = [
  'department',
  'company',
  'user',
  'task',
  'violation',
  'regulation',
]

def fill(model=None):
  """
    Fill specific model, if model not specified, fill all existing models
  """

  if (model != None):
    if model in MODELS_LIST:
      globals()[f'fill_{model}']()
    else:
      raise IndexError(f'No such model "{model}"')
  else:
    fill_all()

def fill_all():
  """
    Fill all models
  """

  for model in MODELS_LIST:
    globals()[f'fill_{model}']()

def fill_department():
  """
    Fill Department model
  """

  departments = Department.objects.all()
  
  if len(departments) == 0:
    organ = Company.objects.all()

    if len(organ) == 0:
      fill_company()

      organ = Company.objects.all()
    
    new_dep = Department(name=f'New department [Organization {organ[0].id}]')
    new_dep.company = organ[0]

    new_dep.save()
    print(f"Created new department: {new_dep}")

def fill_company():
  """
    Fill Company model
  """

  company = Company.objects.all()

  if len(company) == 0:
    new_company = Company(name="New company")

    new_company.save()
    print(f"Created new company: {new_company}")

def fill_user():
  """
    Fill User model
  """

  department = Department.objects.all()
  user = User.objects.all()

  if len(user) == 0:
    if len(department) == 0:
      fill_department()
      department = Department.objects.all()

    username = _get_random_username(randint(5, 15))
    new_user = User(
      username=username,
      fullname="Some Name Yet",
      department=department[0],
      position="Somebody",
      email="some@name.ye",
      telephone="88005553535",
    )

    new_user.save()
    print(f"Created new user: {new_user}")

def _get_random_username(length):
  """
    Returns random username
  """

  result = ''

  for i in range(length):
    result += chr(randint(33, 126))

  return result

def fill_violation():
  """
    Fill Vilation model
  """
  violation = Violation.objects.all()

  if len(violation) == 0:
    new_viol = Violation(species="Нарушение такое", subspecieses="Поднарушение такое")
    
    new_viol.save()
    print(f"Created new violation: {new_viol}")

def fill_regulation():
  new_reg = Regulations()
  
  new_reg.save()

  approval = Regulations(parent=new_reg, status="На рассмотрении", button="Прикрепить акт")
  approval.save()

  approval2 = Regulations(parent=approval, status="На согласовании", button="Прикрепить акт 2")
  agree = Regulations(parent=approval, status="На согласовании", button="Рассмотрено")
  
  agree.save()
  approval2.save()

  completed = Regulations(parent=agree, status="Рассмотрено", button="Согласовать")

  completed.save()

def fill_task():
  """
    Fill Task
  """
  task = Task.objects.all()
  company = Company.objects.all()
  date = datetime.now()
  regulation = Regulations.objects.all()
  user = User.objects.all()
  number = str(randint(1, 999999))
  district = DISTRICT_CHOICES[0][0]

  if len(task) == 0:
    if len(company) == 0:
      fill_company()
      
      company = Company.objects.filter(parent=None)
    
    if len(regulation):
      fill_regulation()
      
      regulation = Regulations.objects.filter(parent=None)

    if len(user):
      fill_user()

      user = User.objects.all()

    new_task = Task(
      company=company[0],
      district=district,
      date=date,
      number=number,
      user=user[0],
      regulation=regulation[0]
    )

    new_task.save()
    print(f"Created new task:")