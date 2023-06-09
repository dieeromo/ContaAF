from django.urls import path
from . import views

urlpatterns =[
    path('registromovimientos/', views.registroMovimientos , name='registroMovimientos'),
    path('resumenmovimientos/', views.resumenMovimientos , name='resumenMovimientos'),
    path('jsonmovimientos/', views.jsonMovimiento , name='jsonMovimientos'),    
]