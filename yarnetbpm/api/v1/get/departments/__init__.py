from django.http import HttpResponse
from django.core import serializers

from department.models import Department
from decorators import GET

@GET
def all(request):
  response = serializers.serialize('json', Department.objects.all())

  return HttpResponse(response, content_type="application/json")