from django.contrib import admin

from .models import Question, Survey

# Register your models here.

admin.site.register(Survey)
admin.site.register(Question)
