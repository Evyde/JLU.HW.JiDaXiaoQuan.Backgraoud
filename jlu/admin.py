from django.contrib import admin

# Register your models here.

from jlu import models
admin.site.register(models.User)