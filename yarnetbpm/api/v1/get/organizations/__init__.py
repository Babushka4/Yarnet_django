from django.http import HttpResponse

from organization.models import Organization
from decorators import GET

@GET
def all(request):
  response = Organization.objects.all().as_json

  return HttpResponse(response, content_type="application/json")