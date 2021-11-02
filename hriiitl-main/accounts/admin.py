from django.contrib import admin

# Register your models here.
from .models import new, employer

admin.site.register(new)
admin.site.register(employer)

