from django.urls import path
from . import views

urlpatterns =[
    path('seleccion/',views.selec_caja_empresa),
    path('cierre/',views.cierresDiarios, name = 'cierre'),
    #path('cierre2/',views.cierresDiarios2),
    path('cierre3/<int:caja_id>/<int:empresa_id>/<str:fecha_consulta>/',views.cierre3, name='cierre3'),
    path('cierresresumen/',views.CierresResumen, name='cierresresumen'), 
    path('mismovimientos/',views.misMovimientos, name = 'mismovimientos'),
    path('todoscierres/',views.todosCierres, name = 'todosCierres'),
    path('detallescierres/<int:cajaid>/<int:empresa_id>/<str:fecha_consulta>',views.detallesCierres, name='detallesCierres'),
]