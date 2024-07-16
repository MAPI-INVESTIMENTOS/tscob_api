from django.contrib import admin
from webapi.models import *

class EmpresaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
class Pedidos_QuitacaoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
class Empresa_QuitacaoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
class QuitacaoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Pedidos_Quitacao, Pedidos_QuitacaoAdmin)
admin.site.register(Empresa_Quitacao, Empresa_QuitacaoAdmin)
admin.site.register(Quitacao, QuitacaoAdmin)
