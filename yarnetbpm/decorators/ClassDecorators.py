from django.core import serializers

def with_json_serialize(cls):
  @property
  def as_json(self, *args, **kwargs):
    return serializers.serialize('json', [self])

  setattr(cls, 'as_json', as_json)

  return cls