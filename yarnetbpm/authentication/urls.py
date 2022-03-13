from django.urls import path, re_path

from .views import LoginView, RegisterView

urlpatterns = [
  re_path(r'login.+?', LoginView.as_view()),
  re_path(r'registration.+?', RegisterView.as_view()),
]