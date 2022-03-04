from django.http import HttpResponse

from company.models import Company
from decorators import GET

@GET
def all(request):
  response = Company.objects.all().as_json

  return HttpResponse(response, content_type="application/json")