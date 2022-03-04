from django.views.generic import TemplateView
from django.shortcuts import redirect

from task.models import Task, DISTRICT_CHOICES, NewTask, NewFields
from regulations.models import Regulations
from company.models import Company
from violation.models import Violation
from user.models import User
from datetime import datetime

class TaskInfo(TemplateView):
  template_name = 'task_info.html'
  model = NewTask

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tasks_list'] = NewTask.objects.all()
    context['field_types'] = NewFields.Types
    
    return context

# Таблица задач
class TaskTable(TemplateView):
  template_name = 'tasks.html'
  model = Task

  def post(self, request, *args, **kwargs):
    _id = int(request.POST.get('next_id'))
    _task_id = int(request.POST.get('task_id'))
    [_task] = Task.objects.filter(pk=_task_id)
    [_regulation] = Regulations.objects.filter(pk=_id)
    _task.regulation = _regulation
    
    _task.save()

    return redirect('/tasks/')

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(**kwargs)
    context['company_list'] = Company.objects.all()
    context['districts'] = DISTRICT_CHOICES
    context['violation_list'] = Violation.objects.all()
    context['user_list'] = User.objects.all()

    if 'id' in kwargs:
      context['task_list'] = self.model.objects.filter(user=kwargs['id'])
    else:
      context['task_list'] = self.model.objects.all()

    return context

# Добавление новой задачи
class AddNewTask(TemplateView):
  model = Task

  def post(self, request, *args, **kwargs):
    user_id = int(request.POST.get('user'))
    company_id = int(request.POST.get('company'))
    district = request.POST.get('district')
    number = request.POST.get('number')
    user = User.objects.filter(pk=user_id)[0]
    company = Company.objects.filter(pk=company_id)[0]
    regulation = Regulations.objects.filter(parent=None)[0]
    new_task = Task(
      company=company,
      user=user,
      district=district,
      number=number,
      regulation=regulation,
      date=datetime.now(),
    )

    new_task.save()

    return redirect('/tasks/')
