from django.http import JsonResponse, HttpResponse

from company.models import Company
from decorators import POST, deserialize_body, body_has

@POST
@deserialize_body
@body_has(['name'])
def add(request):
  body = request.deserialized

  try:
    new_company = Company(
      name=body['name'],
    )

    new_company.save()

    return JsonResponse({ 'ok': True })
  except:
    return HttpResponse('Internal Server Error', status=500)