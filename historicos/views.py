from datetime import datetime, timedelta
from django.shortcuts import render
from general.models import pagoMeses
from cierres.models import CierresCajas
from egresos.models import pagoColaboradores
# Create your views here.

def catalogoHis(request):
    meses = pagoMeses.objects.order_by('id')
    return render (request, 'catalogoHistoricos.html',{
        'meses':meses
    })


def cifras(request):
    if request.method == 'GET':
        fecha_actual = datetime.now().date()
        fecha_inicial = fecha_actual - timedelta(fecha_actual.day) + timedelta(days=1)
        cifrasCierres = CierresCajas.objects.filter(fecha__range=[fecha_inicial,fecha_actual])
        ingresostotalperiodo = 0
        egresostotalperiodo = 0
        for ingresos in cifrasCierres:
            ingresostotalperiodo = ingresostotalperiodo + ingresos.valorIngresos
            egresostotalperiodo = egresostotalperiodo + ingresos.valorEgresos
       
        cifrasPagocolaboradores = pagoColaboradores.objects.filter(fecha_pago__range=[fecha_inicial,fecha_actual])
        pagoColaboradoresTotal= 0
        for col in cifrasPagocolaboradores:
            pagoColaboradoresTotal = pagoColaboradoresTotal + col.valor
        return render (request,'solidcifras.html',{
            'ingresostotalperiodo':ingresostotalperiodo,
            'egresostotalperiodo':egresostotalperiodo,
            'pagoColaboradoresTotal':pagoColaboradoresTotal,
            'fecha_inicio':fecha_inicial,
            'fecha_fin':fecha_actual

        })
    else:
        cifrasCierres = CierresCajas.objects.filter(fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        
        ingresostotalperiodo = 0
        egresostotalperiodo = 0
        for ingresos in cifrasCierres:
            ingresostotalperiodo = ingresostotalperiodo + ingresos.valorIngresos
            egresostotalperiodo = egresostotalperiodo + ingresos.valorEgresos
        
        cifrasPagocolaboradores = pagoColaboradores.objects.filter(fecha_pago__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagoColaboradoresTotal= 0
        for col in cifrasPagocolaboradores:
            pagoColaboradoresTotal = pagoColaboradoresTotal + col.valor

        return render (request, 'solidcifras.html',{
            'ingresostotalperiodo':ingresostotalperiodo,
            'egresostotalperiodo':egresostotalperiodo,
            'pagoColaboradoresTotal':pagoColaboradoresTotal,
            'fecha_inicio':request.POST['fecha_inicio'],
            'fecha_fin':request.POST['fecha_fin'],
        })

