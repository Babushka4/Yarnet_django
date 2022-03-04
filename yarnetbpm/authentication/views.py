from django.shortcuts import render
from django.views.generic import TemplateView

from user.models import User
# Create your views here.

class LoginView(TemplateView):
  template_name = 'login.html'

  def post(self, request):
    user = self.authenticate(request.POST.get('username'), request.POST.get('password'))

  def authenticate(self, username, password):
    user = User.objects.filter(username=username)
    