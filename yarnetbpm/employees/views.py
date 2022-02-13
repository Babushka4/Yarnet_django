# from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from employees.models import Employee

def index(request):
  params = dict(request.GET)
  print(params)
  if (len(params) == 5):
    if ('fullname' not in params):
      return JsonResponse({ "error": "Fullname not specified" })
    if ('department' not in params):
      return JsonResponse({ "error": "Department not specified" })
    if ('position' not in params):
      return JsonResponse({ "error": "Position not specified" })
    if ('email' not in params):
      return JsonResponse({ "error": "Email not specified" })
    if ('telephone' not in params):
      return JsonResponse({ "error": "Telephone not specified" })

    new_empl = Employee(
      fullname=params['fullname'][0],
      department=params['department'][0],
      position=params['position'][0],
      email=params['email'][0],
      telephone=params['telephone'][0],
    )
    new_empl.save()
  
  response = serializers.serialize('json', Employee.objects.all())
  return HttpResponse(response, content_type="application/json")

# Create your views here.
