from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth import logout, authenticate, login

from user.models import User
# Create your views here.

class LoginView(TemplateView):
  template_name = 'login.html'
  next_url = '/'

  def apply_url(self, request):
    next_url = request.GET.get('next')
    
    if (next_url != None and len(next_url) != 0):
      self.next_url = next_url

  def get_context_data(self, next_url=None, **kwargs):
    context = super().get_context_data(**kwargs)
    context['next_url'] = self.next_url

    return context

  def get(self, request, *args, **kwargs):
    self.apply_url(request)

    if not request.user.is_anonymous:
      return redirect(self.next_url)
    
    return render(request, 'login.html', self.get_context_data(next_url=self.next_url))

  def post(self, request):
    self.apply_url(request)

    username = request.POST.get('login')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if not user:
      return render(
        request,
        'login.html',
        { "error_message": "Неверный логин или пароль." }
      )
    
    login(request, user)

    return redirect(self.next_url)
    
class LogoutView(TemplateView):
  def get(self, request, *args, **kwargs):
    logout(request)

    return redirect('/')

class RegisterView(TemplateView):
  template_name = 'registration.html'
  next_url = '/'

  def apply_url(self, request):
    next_url = request.GET.get('next')
    
    if (next_url != None and len(next_url) != 0):
      self.next_url = next_url

  def get_context_data(self, next_url=None, **kwargs):
    context = super().get_context_data(**kwargs)
    context['next_url'] = self.next_url

    return context

  def get(self, request, *args, **kwargs):
    self.apply_url(request)
    
    if not request.user.is_anonymous:
      return redirect(self.next_url)
    
    return render(request, 'registration.html', self.get_context_data(next_url=self.next_url))

  def post(self, request, *args, **kwargs):
    self.apply_url(request)

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

    return redirect(self.next_url)

