from django.http import JsonResponse, HttpResponse

from user.models import User
from department.models import Department
from decorators import POST, deserialize_body, body_has

@POST
@deserialize_body
@body_has([
  'fullname',
  'department_id',
  'position',
  'email',
  'telephone'
])
def add(request):
  body = request.deserialized

  try:
    try:
      department = Department.objects.filter(pk=body['department_id'])

      if (len(department) != 0):
        new_empl = User(
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
    except Exception as e:
      e.with_traceback()
      return HttpResponse('Internal Server Error', status=500)
  except Exception as e:
    e.with_traceback()
    return HttpResponse('Internal Server Error', status=500)