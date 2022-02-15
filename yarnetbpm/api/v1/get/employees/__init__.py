from django.http import HttpResponse
from django.core import serializers

from employees.models import Employee
from decorators import GET

@GET
def all(request):
  response = serializers.serialize('json', Employee.objects.all())

  return HttpResponse(response, content_type="application/json")