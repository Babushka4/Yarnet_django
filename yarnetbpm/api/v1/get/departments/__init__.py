from django.http import HttpResponse

from department.models import Department
from decorators import GET

@GET
def all(request):
  response = Department.objects.all().as_json

  return HttpResponse(response, content_type="application/json")