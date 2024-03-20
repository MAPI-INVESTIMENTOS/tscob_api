from django.contrib import admin
from webapi.models import *
# Register your models here.
admin.site.register(Empresa)

admin.site.register(Pedidos_Quitacao)
admin.site.register(Empresa_Quitacao)

admin.site.register(Quitacao)