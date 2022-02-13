import json

from django.http import HttpResponse

def deserialize_body(fn):
  def wrap(request, *args, **kwargs):
    deserialized = None;

    try:
      deserialized = json.loads(request.body)
      
      setattr(request, 'deserialized', deserialized)
    except:
      return HttpResponse('Bad Request', status=400)
    
    return fn(request, *args, **kwargs)

  return wrap
  

def body_has(fields_list):
  def func_wrap(fn):
    def wrap(request, *args, **kwargs):
      for field in fields_list:
        if (field not in request.deserialized):
          return HttpResponse('Bad Request', status=400)

      return fn(request, *args, **kwargs)
    
    return wrap

  return func_wrap