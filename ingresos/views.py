from datetime import datetime, timedelta
from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from . models import ingresosCajas
from . forms import form_registroIngresos
from general.models import cajasReg, empresa

# Create your views here.
def registroIngresos(request):
    if request.method == 'GET':
        return render(request, 'registroIngresos.html',{
            'form':form_registroIngresos
        })
    else:
        form2 = form_registroIngresos(request.POST)
        #form2 = form_registroIngresos(empresaIngreso=request.POST['empresaIngreso'], conceptoIngreso=request.POST['conceptoIngreso'],valorIngreso=request.POST['valorIngreso'],descripcion=request.POST['descripcion'])
        nuevo_reg_ingreso = form2.save(commit=False)
        
        caja_reg_ingreso = cajasReg.objects.get(usuario=request.user)
        print(caja_reg_ingreso)

        nuevo_reg_ingreso.nombreCaja =caja_reg_ingreso
        nuevo_reg_ingreso.usuario = request.user
        nuevo_reg_ingreso.fecha = request.POST['fecha']
        nuevo_reg_ingreso.save()

   
        return redirect('resumenIngresos')
    

def resumenIngresos(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=0)
    ingresosConsulta = ingresosCajas.objects.filter(fecha__range=[fecha_inicial,fecha_actual])

    return render(request, 'resumenIngresos.html',{
        'ingresosConsulta':ingresosConsulta,
    })

def JsonIngresos(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=0)
    ingresosConsulta = ingresosCajas.objects.filter(fecha__range=[fecha_inicial,fecha_actual])
    listaIngresos = []
    for ing in ingresosConsulta:
        dataIngresos = {}
        dataIngresos['nombreCaja']= str(ing.nombreCaja)
        dataIngresos['empresaIngreso']=str(ing.empresaIngreso)
        dataIngresos['valorIngreso']=ing.valorIngreso
        dataIngresos['conceptoIngreso']=str(ing.conceptoIngreso)
        dataIngresos['fecha']=ing.fecha
        dataIngresos['descripcion']=ing.descripcion
        listaIngresos.append(dataIngresos)
    return JsonResponse({'listaIngresos':listaIngresos}, safe=False)
