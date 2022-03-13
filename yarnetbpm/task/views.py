import json

from datetime import datetime
from django.views.generic import TemplateView
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from task.models import History, Task, Fields, Values
from regulations.models import Regulations
from company.models import Company
from violation.models import Violation
from user.models import User
from decorators import POST

class TaskInfo(LoginRequiredMixin, TemplateView):
  template_name = 'task_info.html'
  model = Task

  def get(self, request, *args, **kwargs):
    print(request.user)
    if (request.user.is_anonymous):
      print('Anonymus')
      user = authenticate(username='Gy', password='asdf')
      if not user:
        print('fixme')
      else:
        login(request, user)
        print('authed')
    else:
      print('alredy registered :)')

    return HttpResponse(self.get_context_data())

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tasks_list'] = Task.objects.all()
    context['field_types'] = Fields.Types
    
    return context

# Таблица задач
class TaskTable(LoginRequiredMixin, TemplateView):
  template_name = 'tasks.html'
  model = Task

  def post(self, request, *args, **kwargs):
    _id = int(request.POST.get('next_id'))
    _task_id = int(request.POST.get('task_id'))
    [_task] = Task.objects.filter(pk=_task_id)
    [_stage] = Regulations.Stage.objects.filter(pk=_id)
    _old_stage = _task.stage
    _task.stage = _stage
    
    if len(_task.stage.childs) == 0:
      _task.is_completed = True

    _task.save()

    History.objects.new_record(
      _task, 
      _task.stage,
      f"{_task.stage.button_name}: {_old_stage.title} => {_task.stage.title}.",
      request.user,
    )

    return redirect('/tasks/')

  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(**kwargs)
    context['company_list'] = Company.objects.all()
    context['districts'] = Task.District.choices
    context['violation_list'] = Violation.objects.all()
    context['user_list'] = User.objects.all()
    context['stage_schemes'] = Regulations.Stage.Types
    context['field_types'] = Fields.Types
    context['regulations_list'] = Regulations.objects.all()

    if 'id' in kwargs:
      context['task_list'] = self.model.objects.filter(user=kwargs['id'], is_completed=False).order_by('pk')
    else:
      context['task_list'] = self.model.objects.filter(is_completed=False).order_by('pk')

    return context

# Добавление новой задачи
class AddNewTask(LoginRequiredMixin, TemplateView):
  def post(self, request, *args, **kwargs):
    task_name = request.POST.get('task_name')
    reg_id = int(request.POST.get('reg_id'))
    task_performer = int(request.POST.get('task_performer'))
    [regulations] = Regulations.objects.filter(pk=reg_id)
    [task_performer] = User.objects.filter(pk=task_performer)
    [author, *_] = User.objects.all()
    values = []
    fields = regulations.first_stage.fields_set.all()
    _class = {
      Fields.Types.USER: User,
      Fields.Types.COMPANY: Company,
    }
    new_task = Task(
      name=task_name,
      regulations=regulations,
      stage=regulations.first_stage,
      author=author,
      performer=task_performer,
    )

    new_task.save()

    for field in fields:
      posted_value = request.POST.get(f"value_{field.id}")
      correct_value = posted_value

      if field.field_type == Fields.Types.DATE:
        correct_value = datetime.strptime(posted_value, '%H:%M %m.%d.%Y')

      if field.field_type in [Fields.Types.USER, Fields.Types.COMPANY]:
        correct_value = int(correct_value)
        [correct_value] = _class[field.field_type].objects.filter(pk=correct_value)

      new_value = Values(field=field, value=correct_value, task=new_task)
      new_value.save()
      values.append(new_value)

    History.objects.new_record(
      new_task, 
      new_task.stage,
      'Новая задача.',
      request.user,
    )
    
    return redirect('/tasks/')

class ReassignPerformer(LoginRequiredMixin, TemplateView):
  def post(self, request, *args, **kwargs):
    _task_id = int(request.POST.get('task_id'))
    _reassign_to = int(request.POST.get('reassign_to'))
    [_task] = Task.objects.filter(pk=_task_id)
    [_user] = User.objects.filter(pk=_reassign_to)
    
    if _task.performer.id != _user.id:
      _old_performer = _task.performer
      _task.performer = _user

      _task.save()
      History.objects.new_record(
        _task,
        _task.stage,
        f"Изменён исполнитель: {_old_performer.fullname} => {_user.fullname}.",
        request.user,
      )
    
    return redirect('/tasks/')


@POST
@login_required
def get_form(request):
  regulations_id = request.POST.get('id')
  t = loader.get_template('create_new_task_content.html')
  render_data = {
    'reg_list': Regulations.objects.all(),
    'regulations': Regulations.objects.filter(pk=regulations_id)[0],
    'field_types': Fields.Types,
    'all_users': User.objects.all(),
    'all_companies': Company.objects.all(),
  }
  html = t.render(render_data, request=request)

  return HttpResponse(json.dumps({'html': html}), 'application/json')

@POST
@login_required
def get_sidebar_body(request):
  t = loader.get_template('task_creator_sidebar.html')
  render_data = {
    'regulations_list': Regulations.objects.all(),
  }
  html = t.render(render_data, request=request)

  return HttpResponse(json.dumps({'html': html}), 'application/json')

@POST
@login_required
def get_view_task_body(request):
  task_id = request.POST.get('task_id')
  [task] = Task.objects.filter(pk=task_id)
  temp = loader.get_template('task_view.html')
  render_data = {
    'task': task,
    'all_users': User.objects.all(),
    'field_types': Fields.Types,
    'stage_schemes': Regulations.Stage.Types,
  }
  html = temp.render(render_data, request=request)

  return HttpResponse(json.dumps({ 'html': html }), 'application/json')

@POST
@login_required
def get_view_task_history(request):
  task_id = request.POST.get('task_id')
  [task] = Task.objects.filter(pk=task_id)
  history = History.objects.group_by_date(task)
  temp = loader.get_template('task_view_history.html')
  render_data = {
    'task': task,
    'history': history,
  }
  html = temp.render(render_data, request=request)

  return HttpResponse(json.dumps({ 'html': html }), 'application/json')