from django.urls import path
from . import views

urlpatterns =[
    path('homeinventario/', views.homeInventario , name='homeInventario'),
    path('ingresoinvretiro/', views.ingresosInvRetiros , name='ingresosInvRetiros'),
    path('resumeninginvretiros/', views.ResumenIngInvRetiros , name='ResumenIngInvRetiros'),
    path('registroinventariofacturas/', views.ingresosInvFacturas , name='ingresosInvFacturas'),
    path('resumeninvfacturas/<int:idfactura>', views.ResumenInvFacturas , name='ResumenInvFacturas'),
    path('registrosalidainstalaciones/', views.ResgistroSalidaInstalacion , name='ResgistroSalidaInstalacion'),
    path('resumensalidainstalaciones/', views.ResumenSalidaInstalacion , name='ResumenSalidaInstalacion'),
    path('precierre/', views.preCierreInventario , name='preCierreInventario'),

    path('registrosalidaventascontado/', views.RegistroSalidaVentasContado , name='RegistroSalidaVentasContado'),
    path('resumensalidaventascontado//', views.ResumenSalidaVentasContado , name='ResumenSalidaVentasContado'),
   


]
