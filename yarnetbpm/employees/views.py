from django.views.generic import TemplateView

from employees.models import Employee
from department.models import Department

class EmployeeTable(TemplateView):
  template_name = 'employee_table.html'
  model = Employee

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['employee_list'] = self.model.objects.all()

    return context