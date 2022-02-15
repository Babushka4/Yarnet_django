from django.urls import path

from . import views

urlpatterns = [
    path('v1/employees/', views.get_employees, name='get_employees'),
    path('v1/employees/add/', views.add_employees, name='add_employees'),

    path('v1/departments/', views.get_departments, name='get_departments'),
    path('v1/departments/add/', views.add_departments, name='add_departments'),

    path('v1/organizations/', views.get_organizations, name='get_organizations'),
    path('v1/organizations/add/', views.add_organizations, name='add_organizations')
]