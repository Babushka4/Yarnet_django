from django.urls import path

from . import v1

urlpatterns = [
    path('v1/employees/', v1.get.users.all, name='get_employees'),
    path('v1/employees/add/', v1.post.users.add, name='add_employees'),

    path('v1/departments/', v1.get.departments.all, name='get_departments'),
    path('v1/departments/add/', v1.post.departments.add, name='add_departments'),

    path('v1/companies/', v1.get.companies.all, name='get_companies'),
    path('v1/companies/add/', v1.post.companies.add, name='add_companies'),
]