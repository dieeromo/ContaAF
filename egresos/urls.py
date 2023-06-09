from django.urls import path
from . import views

urlpatterns =[
    path('catalogoregistroegresos/', views.catalogoRegistroEgresos , name='CatalogoRegistroEgresos'),
    
    path('registrofacturas/', views.registroFacturas , name='RegistroFacturas'),
    path('resumenregfacturas/', views.resumenRegistroFacturas , name='ResumenRegistroFacturas'),
    path('jsonfacturas/',views.json_facturas,name='jsonfacturas'),
    
    path('registropagocolaboradores/', views.registroPagoColaboradores , name='RegistroPagoColaboradores'),
    path('resumenpagocolaboradores/', views.resumenPagoColaboradores , name='ResumenPagoColaboradores'),
    path('jsoncolaboradores/',views.jsonColaboradores,name='jsonColaboradores'),

    path('registropagoservicios/', views.registroPagoServicios, name='RegistroPagoServicios'),
    path('resumenpagoservicios/', views.resumenPagoServicios, name='ResumenPagoServicios'),
    path('jsonpagoservicios/', views.JsonPagoServicios, name='jsonpagoservicios'),

    path('registropagocreditos/', views.registroPagoCreditos, name='RegistroPagoCreditos'),
    path('resumenpagocreditos/', views.resumenPagoCredito, name='ResumenPagoCredito'),
    path('jsonpagocreditos/', views.JsonPagoCreditos, name='JsonPagoCredito'),


    path('registropagodecimos/', views.registroPagoDecimos, name='RegistroPagoDecimos'),
    path('resumenpagodecimos/', views.resumenPagoDecimos, name='ResumenPagoDecimos'),
    path('jsonpagodecimos/', views.jsonPagoDecimos, name='jsonPagoDecimos'),

    

    path('registropagoiess/', views.registroPagoIess, name='RegistroPagoIess'),
    path('resumenpagoiess/', views.resumenPagoIess, name='ResumenPagoIess'),
    path('jsonpagoiess/', views.jsonPagoIess, name='jsonPagoIess'),

    
]