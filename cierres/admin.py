from django.contrib import admin
from . models import CierresCajas

class CierresAdmin(admin.ModelAdmin):
    list_display = ( 'fecha','empresa','caja','valorIngresos','valorEgresos','valorMovSalida','valorMovEntrada','valorCierreAnterior', 'valorCierreActual')
    list_filter = ('empresa','caja')
admin.site.register(CierresCajas,CierresAdmin)
