from django.urls import path

from . import views

urlpatterns = [
    path('v1/employees/', views.get_employees, name='get_employees'),
    path('v1/employees/add/', views.add_employees, name='add_employees')
]