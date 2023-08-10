from django.urls import path
from . import views

urlpatterns =[
    path('homeinventario/', views.homeInventario , name='homeInventario'),

    
]