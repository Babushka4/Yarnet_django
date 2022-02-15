from django.http import HttpResponse
from django.core import serializers

from organization.models import Organization
from decorators import GET

@GET
def all(request):
  response = serializers.serialize('json', Organization.objects.all())

  return HttpResponse(response, content_type="application/json")