from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.ProxyService)
admin.site.register(models.Category)
admin.site.register(models.ProxyServiceTransactions)
admin.site.register(models.Methods)