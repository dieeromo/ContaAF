from django.urls import path
from . import views

urlpatterns =[
    path('homeinventario/', views.homeInventario , name='homeInventario'),
    path('ingresoinvretiro/', views.ingresosInvRetiros , name='ingresosInvRetiros'),
    path('resumeninginvretiros/', views.ResumenIngInvRetiros , name='ResumenIngInvRetiros'),
    path('registroinventariofacturas/', views.ingresosInvFacturas , name='ingresosInvFacturas'),
    path('preresumeninventariofacturas/', views.PreResumenInvFacturas , name='PreResumenInvFacturas'),
    path('resumeninvfacturas/<int:idfactura>', views.ResumenInvFacturas , name='ResumenInvFacturas'),

    path('registrosalidainstalaciones/', views.ResgistroSalidaInstalacion , name='ResgistroSalidaInstalacion'),
    path('resumensalidainstalaciones/', views.ResumenSalidaInstalacion , name='ResumenSalidaInstalacion'),
   

    path('registrosalidaventascontado/', views.RegistroSalidaVentasContado , name='RegistroSalidaVentasContado'),
    path('resumensalidaventascontado//', views.ResumenSalidaVentasContado , name='ResumenSalidaVentasContado'),

    path('registromovimientosinv/', views.registroMovimientosInv , name='registroMovimientosInv'),
    path('resumenmovimientosinv/', views.resumenMovimientosInv , name='resumenMovimientosInv'),

     path('precierre/', views.preCierreInventario , name='preCierreInventario'),
     path('registrocierrebodega/<int:idBodega>/<str:fecha>/<int:id_empresa>', views.cierreInventarioBodega , name='cierreInventarioBodega'),
     path('resumencierrebodega/', views.ResumenCierreInventarioBodega , name='ResumenCierreInventarioBodega'),

     path('registroclientes/', views.RegistroClientes , name='RegistroClientes'),
     path('resumenclientes/', views.ResumenClientes , name='ResumenClientes'),
     
     path('actualizacion/', views.actualizacionFacturas , name='actualizacionFacturas'),

     
    
   


]
