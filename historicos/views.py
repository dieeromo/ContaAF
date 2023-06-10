from django.shortcuts import render
from general.models import pagoMeses
# Create your views here.

def catalogoHis(request):
    meses = pagoMeses.objects.order_by('id')
    return render (request, 'catalogoHistoricos.html',{
        'meses':meses
    })
