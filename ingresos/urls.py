from django.urls import path
from . import views

urlpatterns =[
    path('registroingresos/',views.registroIngresos, name='registroIngresos'),
   
    path('resumeningresos/',views.resumenIngresos, name='resumenIngresos'),
    path('jsoningresos/',views.JsonIngresos, name='JsonIngresos'),
]