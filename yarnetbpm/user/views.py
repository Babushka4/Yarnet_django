from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import User


class UserTable(LoginRequiredMixin, TemplateView):
  template_name = 'user_table.html'
  model = User

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['user_list'] = self.model.objects.all()

    return context