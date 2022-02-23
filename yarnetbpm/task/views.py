from django.views.generic import TemplateView

from task.models import Task

# Create your views here.
class TaskTable(TemplateView):
  template_name = 'tasks.html'
  model = Task

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['task_list'] = self.model.objects.all()

    return context