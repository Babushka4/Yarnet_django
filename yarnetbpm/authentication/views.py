from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from user.models import User
# Create your views here.

class LoginView(TemplateView):
  template_name = 'login.html'

  def get_context_data(self, **kwargs):
      return super().get_context_data(**kwargs)

  def post(self, request):
    user = self.authenticate(request.POST.get('username'), request.POST.get('password'))

  def authenticate(self, username, password):
    user = User.objects.filter(username=username)
    
class RegisterView(TemplateView):
  template_name = 'registration.html'

  def get(self, request, *args, **kwargs):
    if not request.user.is_anonymous:
      return redirect('/')
    
    return render(request, 'registration.html')

  def post(self, request, *args, **kwargs):
    login = request.POST.get('login')
    user = User.objects.filter(username=login)

    if user:
      return render(
        request,
        'registration.html',
        { "error_message": "Такой пользователь уже существует." }
      )
    
    email = request.POST.get('email')
    password = request.POST.get('password')
    telephone = request.POST.get('telephone')
    fullname = request.POST.get('fullname')
    user = User.objects.create_user(login, password)
    user.telephone = telephone
    user.email = email
    user.fullname = fullname

    user.save()

    return redirect('/')

