from django.shortcuts import render

# Create your views here.

def homeInventario(request):
    return render (request, 'home_inventario.html')
