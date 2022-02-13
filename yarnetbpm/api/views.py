from django.http import JsonResponse, HttpResponse
from django.core import serializers

from employees.models import Employee
from decorators import GET, POST, deserialize_body, body_has

@GET
def get_employees(request):
  response = serializers.serialize('json', Employee.objects.all())

  return HttpResponse(response, content_type="application/json")

@POST
@deserialize_body
@body_has([
  'fullname',
  'department',
  'position',
  'email',
  'telephone'
])
def add_employees(request):
  body = request.deserialized

  try:
    new_empl = Employee(
      fullname=body['fullname'],
      department=body['department'],
      position=body['position'],
      email=body['email'],
      telephone=body['telephone'],
    )

    new_empl.save()

    return JsonResponse({ 'ok': True })
  except:
    return HttpResponse('Internal Server Error', status=500)
