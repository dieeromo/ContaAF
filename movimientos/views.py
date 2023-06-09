from datetime import datetime, timedelta
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from . forms import form_movimientos
from general.models import cajasReg
from . models import movimientos

# Create your views here.
def registroMovimientos(request):
    if request.method == 'GET':
        return render(request, 'registroMovimientos.html',{
            'form': form_movimientos,
        })
    else:
        form2 = form_movimientos(request.POST)
        nuevo_reg_mov = form2.save(commit=False)

        caja_origen_mov = cajasReg.objects.get(usuario=request.user)

        nuevo_reg_mov.caja_origen = caja_origen_mov
        nuevo_reg_mov.fecha = request.POST['fecha']
        nuevo_reg_mov.usuario = request.user

        nuevo_reg_mov.save()

        return redirect('resumenMovimientos')
    
def resumenMovimientos(request):

    return render(request,'resumenMovimientos.html' )


def jsonMovimiento(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=0)
    caja_Mov = cajasReg.objects.get(usuario=request.user)
    cajassMovimiento = movimientos.objects.filter(fecha__range=[fecha_inicial,fecha_actual],caja_origen=caja_Mov)
    ListaMovimientos = []
    for lism in cajassMovimiento:
        dataMov = {}
        dataMov['empresaCaja'] = str(lism.empresaCaja)
        dataMov['caja_destino'] = str(lism.caja_destino)
        dataMov['valor'] = lism.valor
        dataMov['fecha'] = lism.fecha
        dataMov['descripcion'] = lism.descripcion
        ListaMovimientos.append(dataMov)

    
    return JsonResponse({'ListaMovimientos':ListaMovimientos}, safe=False)