from django.http import JsonResponse, HttpResponse
from django.core import serializers

from employees.models import Employee
from department.models import Department
from organization.models import Organization
from decorators import GET, POST, deserialize_body, body_has

@GET
def get_employees(request):
  response = serializers.serialize('json', Employee.objects.all())

  return HttpResponse(response, content_type="application/json")

@GET
def get_departments(request):
  response = serializers.serialize('json', Department.objects.all())

  return HttpResponse(response, content_type="application/json")

@GET
def get_organizations(request):
  response = serializers.serialize('json', Organization.objects.all())

  return HttpResponse(response, content_type="application/json")

@POST
@deserialize_body
@body_has([
  'name',
  'organizations'
])
def add_departments(request):
  body = request.deserialized

  try:
    try:
      organizations = Organization.objects.filter(pk__in=body['organizations'])

      if (len(organizations) != 0):
        new_department = Department(
          name=body['name'],
          organizations=organizations
        )

        new_department.save()

        return JsonResponse({ 'ok': True })
      else:
        return JsonResponse({ 'ok': False, 'message': 'No such organizations' }, status=400)
    except:
      return HttpResponse('Internal Server Error', status=500)
  except:
    return HttpResponse('Internal Server Error', status=500)

@POST
@deserialize_body
@body_has(['name'])
def add_organizations(request):
  body = request.deserialized

  try:
    new_organization = Organization(name=body['name'])

    new_organization.save()

    return JsonResponse({ 'ok': True })
  except:
    return HttpResponse('Internal Server Error', status=500)

@POST
@deserialize_body
@body_has([
  'fullname',
  'department_id',
  'position',
  'email',
  'telephone'
])
def add_employees(request):
  body = request.deserialized

  try:
    try:
      department = Department.objects.filter(pk=body['department_id'])

      if (len(department) != 0):
        new_empl = Employee(
          fullname=body['fullname'],
          department=department[0],
          position=body['position'],
          email=body['email'],
          telephone=body['telephone'],
        )

        new_empl.save()

        return JsonResponse({ 'ok': True })
      else:
        return JsonResponse({ 'ok': False, 'message': 'No such department' }, status=400)
    except:
      return HttpResponse('Internal Server Error', status=500)
  except:
    return HttpResponse('Internal Server Error', status=500)