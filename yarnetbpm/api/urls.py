from django.urls import path

from . import v1

urlpatterns = [
    path('v1/employees/', v1.get.employees.all, name='get_employees'),
    path('v1/employees/add/', v1.post.employees.add, name='add_employees'),

    path('v1/departments/', v1.get.departments.all, name='get_departments'),
    path('v1/departments/add/', v1.post.departments.add, name='add_departments'),

    path('v1/organizations/', v1.get.organizations.all, name='get_organizations'),
    path('v1/organizations/add/', v1.post.organizations.add, name='add_organizations')
]