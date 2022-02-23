from django.contrib import admin

# Register your models here.
from violation.models import Violation

admin.site.register(Violation)