from django.http import HttpResponse

def method(method):
  def func_wrap(fn):
    def wrap(request, *args, **kwargs):
      if (request.method == method):
        return fn(request, *args, **kwargs)
      else:
        return HttpResponse('Not found', status=404)

    return wrap

  return func_wrap

def POST(fn):
  @method('POST')
  def wrap(*args, **kwargs):
    return fn(*args, **kwargs)

  return wrap

def GET(fn):
  @method('GET')
  def wrap(*args, **kwargs):
    return fn(*args, **kwargs)

  return wrap

def DELETE(fn):
  @method('DELETE')
  def wrap(*args, **kwargs):
    return fn(*args, **kwargs)

  return wrap

def request_has(prop):
  def func_wraper(fn):
    def wrap(request, *args, **kwargs):
      if (hasattr(request, prop)):
        return fn(request, *args, **kwargs)
      else:
        return HttpResponse('Bad Request', status=400)

    return wrap

  return func_wraper

def header(header, value=None):
  def func_wraper(fn):
    @request_has('headers')
    def wrap(request, *args, **kwargs):
      if (value == None):
        if (header in request.headers):
          return fn(request, *args, **kwargs)
        else:
          return HttpResponse('Authentication Timeout', status=419)
      else:
        if (header in request.headers and request.header[header] == value):
          return fn(request, *args, **kwargs)
        else:
          return HttpResponse('Authentication Timeout', status=419)

    return wrap

  return func_wraper
