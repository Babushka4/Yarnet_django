from django.http import HttpResponse

from user.models import User
from decorators import GET

@GET
def all(request):
  response = User.objects.all().as_json

  return HttpResponse(response, content_type="application/json")