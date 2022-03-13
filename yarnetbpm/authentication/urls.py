from django.urls import path

from .views import LoginView, RegisterView

urlpatterns = [
  path('login', LoginView.as_view()),
  path('registration', RegisterView.as_view()),
]