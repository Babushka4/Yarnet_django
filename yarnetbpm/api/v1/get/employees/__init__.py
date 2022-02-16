from django.http import HttpResponse

from employees.models import Employee
from decorators import GET

@GET
def all(request):
  response = Employee.objects.all().as_json

  return HttpResponse(response, content_type="application/json")