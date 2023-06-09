from django.urls import path
from . import views

urlpatterns =[
    path('',views.home,name='home'),
    path('signup/',views.signup),
    path('task/',views.task, name='task'),
    path('logout/',views.signout, name='logout'),
    path('signin/',views.signin,name='signin')

]