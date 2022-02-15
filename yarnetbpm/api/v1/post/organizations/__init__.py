from django.http import JsonResponse, HttpResponse

from organization.models import Organization
from decorators import GET, POST, deserialize_body, body_has

@POST
@deserialize_body
@body_has(['name'])
def add(request):
  body = request.deserialized

  try:
    new_organization = Organization(name=body['name'])

    new_organization.save()

    return JsonResponse({ 'ok': True })
  except:
    return HttpResponse('Internal Server Error', status=500)