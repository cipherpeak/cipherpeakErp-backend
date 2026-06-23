from django.contrib import admin

from .models import Note, Meeting

# Register your models here.

admin.site.register(Note)
admin.site.register(Meeting)