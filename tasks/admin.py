from django.contrib import admin
from .models import Task, TaskImage
# Register your models here.
admin.site.register(Task)
admin.site.register(TaskImage)