# from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from employees.models import Employee
from random import randint

def index(request):
  params = dict(request.GET)
  if (len(params) == 5):
    if ('fullname' not in params):
      return HttpResponse('{ "error": "Fullname not specified" }')
    if ('department' not in params):
      return HttpResponse('{ "error": "Department not specified" }')
    if ('position' not in params):
      return HttpResponse('{ "error": "Position not specified" }')
    if ('email' not in params):
      return HttpResponse('{ "error": "Email not specified" }')
    if ('telephone' not in params):
      return HttpResponse('{ "error": "Telephone not specified" }')

    new_empl = Employee(
      fullname=params['fullname'],
      department=params['department'],
      position=params['position'],
      email=params['email'],
      telephone=params['telephone'],
    )
    new_empl.save()

  return HttpResponse(serializers.serialize('json', Employee.objects.all()))

# Create your views here.
