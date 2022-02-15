from django.http import JsonResponse, HttpResponse

from department.models import Department
from organization.models import Organization
from decorators import POST, deserialize_body, body_has

@POST
@deserialize_body
@body_has([
  'name',
  'organizations'
])
def add(request):
  body = request.deserialized

  try:
    try:
      organizations = Organization.objects.filter(pk__in=body['organizations'])

      if (len(organizations) != 0):
        new_department = Department(name=body['name'])

        new_department.save()
        new_department.organizations.add(*organizations)
        new_department.save()

        return JsonResponse({ 'ok': True })
      else:
        return JsonResponse({ 'ok': False, 'message': 'No such organizations' }, status=400)
    except Exception as e:
      e.with_traceback()
      return HttpResponse('Internal Server Error', status=500)
  except Exception as e:
    e.with_traceback()
    return HttpResponse('Internal Server Error', status=500)