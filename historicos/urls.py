from django.urls import path
from . import views

urlpatterns =[
    path('catalogohistoricos/',views.catalogoHis, name='catalogoHis'),
   
]