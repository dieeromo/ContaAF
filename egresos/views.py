from datetime import datetime, timedelta
from django.utils.dateparse import parse_date
#import json
#from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from . forms import form_registroFacturas, form_pagoColaboradores, form_pagoServicios
from . forms import form_PagoCreditos, form_pagoDecimos, form_planillasIess
from general.models import cajasReg
from . models import facturasProveedores, pagoColaboradores, pagoServicios, pagoCreditos
from .models import decimos, planillasIESS

# Create your views here.
def is_valid_date(date_string):
    try:
        parse_date(date_string)
        print(parse_date(date_string))
        return True
    except ValueError:
        print("fecha invalida")
        return False


def catalogoRegistroEgresos(request):
    return render(request, 'catalogoRegistroEgresos.html')


def registroFacturas(request):
    if request.method == 'GET':
        return render(request, 'registroFacturas.html',{
            'form':form_registroFacturas,
        })
    else:
        form2 = form_registroFacturas(request.POST)
        nuevo_regfactura = form2.save(commit=False)

        caja_regfactura = cajasReg.objects.get(usuario=request.user)
        nuevo_regfactura.estadoEntrega = False
        nuevo_regfactura.fechafactura = request.POST['fecha_factura']
        
        nuevo_regfactura.id_caja = caja_regfactura
        nuevo_regfactura.id_usuario = request.user

        print(request.POST['fechapago'])
        #if is_valid_date(request.POST['fechapago']):
        #    nuevo_regfactura.fechapago = request.POST['fechapago']
        #    print("guardo fecha")

        if parse_date(request.POST['fechapago']) is not None:
            nuevo_regfactura.fechapago = request.POST['fechapago']
        nuevo_regfactura.save()
        return redirect('ResumenRegistroFacturas')

def resumenRegistroFacturas(request):
    #return render(request, 'resumenRegistroFacturas.html')
    return render(request, 'resumenFacturas.html')

def json_facturas(request):
    #facturasConsulta = facturasProveedores.objects.all()
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=0)
    caja_fac = cajasReg.objects.get(usuario=request.user)
    facturasConsulta = facturasProveedores.objects.filter(fechapago__range=[fecha_inicial,fecha_actual],id_caja=caja_fac)
    listaFacturas = []
    for fac in facturasConsulta:
        data_factura = {}
        data_factura['idproveedor']= str(fac.idproveedor)
        data_factura['numeroFactura']=fac.numeroFactura
        data_factura['fechafactura']=fac.fechafactura
        data_factura['fechapago']=fac.fechapago
        data_factura['valor']=fac.valor
        data_factura['id_modoCompra']=str(fac.id_modoCompra)
        data_factura['id_caja']=str(fac.id_caja)
        listaFacturas.append(data_factura)
    return JsonResponse({'listaFacturas':listaFacturas}, safe=False)

def registroPagoColaboradores(request):
    if request.method == 'GET':
        return render(request, 'registroPagoColaboradores.html',{
            'form':form_pagoColaboradores
        })
    else:
        form2 = form_pagoColaboradores(request.POST)
        nuevo_PagoColaboradores = form2.save(commit=False)

        caja_pagoColaboradores = cajasReg.objects.get(usuario=request.user)
        nuevo_PagoColaboradores.id_caja = caja_pagoColaboradores
        nuevo_PagoColaboradores.id_usuario = request.user
        nuevo_PagoColaboradores.fecha_pago = request.POST['fecha_pago']

        nuevo_PagoColaboradores.save()

        return redirect('ResumenPagoColaboradores')
    
def jsonColaboradores(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=0)
    caja_col = cajasReg.objects.get(usuario=request.user)
    
    colaboradoresConsulta = pagoColaboradores.objects.filter(fecha_pago=fecha_actual,id_caja=caja_col)
    
    
    listaPagoColaboradores = []
    for pagoCol in colaboradoresConsulta:
        dataPagoCol = {}
        dataPagoCol['nombre']=str(pagoCol.nombre)
        dataPagoCol['descripcion']= pagoCol.descripcion
        dataPagoCol['dias_normales']= pagoCol.dias_normales
        dataPagoCol['dias_extras']= pagoCol.dias_extras
        dataPagoCol['dias_feriados']= pagoCol.dias_feriados
        dataPagoCol['fecha_pago']= pagoCol.fecha_pago
        dataPagoCol['valor']= pagoCol.valor
        dataPagoCol['id_caja']= str(pagoCol.id_caja)
        dataPagoCol['id_empresa']= str(pagoCol.id_empresa)
        listaPagoColaboradores.append(dataPagoCol)
    return JsonResponse({'listaPagoColaboradores':listaPagoColaboradores}, safe=False)

def resumenPagoColaboradores(request):
    return render(request,'resumenPagoColaboradores.html')

def registroPagoServicios(request):
    if request.method == 'GET':
        return render(request, 'registroPagoServicios.html',{
            'form':form_pagoServicios,
        })
    else:
        form2 = form_pagoServicios(request.POST)
        nuevo_pago_serv = form2.save(commit=False)

        caja_reg_servicio = cajasReg.objects.get(usuario=request.user)
        nuevo_pago_serv.caja = caja_reg_servicio
        nuevo_pago_serv.usuario = request.user
        nuevo_pago_serv.fecha = request.POST['fecha']

        nuevo_pago_serv.save()

        return redirect('ResumenPagoServicios')

def JsonPagoServicios(request):
    caja_ser = cajasReg.objects.get(usuario=request.user)
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=0)
    PagoServiciosConsulta = pagoServicios.objects.filter(fecha__range=[fecha_inicial,fecha_actual], caja=caja_ser).order_by('-fecha')
    ListaPagoServicios = []
    for pagoSer in PagoServiciosConsulta:
        dataServicios = {}
        dataServicios['servicio'] = str(pagoSer.servicio)
        dataServicios['empresa_servicio'] = str(pagoSer.empresa_servicio)
        dataServicios['empresa_nuestra'] = str(pagoSer.empresa_nuestra)
        dataServicios['mes_de_Pago'] = str(pagoSer.mes_de_Pago)
        dataServicios['anio_de_pago'] = str(pagoSer.anio_de_pago)
        dataServicios['valor'] = pagoSer.valor
        dataServicios['fecha'] = pagoSer.fecha
        dataServicios['descripcion'] = pagoSer.descripcion
        dataServicios['caja'] =  str(pagoSer.caja)
        ListaPagoServicios.append(dataServicios)
    return JsonResponse({'ListaPagoServicios':ListaPagoServicios}, safe=False)

def resumenPagoServicios(request):
    return render(request, 'resumenPagoServicios.html')

def registroPagoCreditos(request):
    if request.method == 'GET':

         return render(request, 'registroPagoCreditos.html',{
             'form':form_PagoCreditos,
         })
    else:
        form2 = form_PagoCreditos(request.POST)
        nuevo_regPagoCredito = form2.save(commit=False)

        caja_reg_credito = cajasReg.objects.get(usuario=request.user)

        nuevo_regPagoCredito.caja = caja_reg_credito
        nuevo_regPagoCredito.usuario = request.user
        nuevo_regPagoCredito.fecha = request.POST['fecha']
        nuevo_regPagoCredito.save()

        return redirect('ResumenPagoCredito')

def JsonPagoCreditos(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=0)
    pagoCreditosConsulta = pagoCreditos.objects.filter(fecha__range=[fecha_inicial,fecha_actual]).order_by('-fecha')
    ListaPagoCreditos = []
    for pagoCre in pagoCreditosConsulta:
        dataCreditos = {}
        dataCreditos['nombre_coop'] = str(pagoCre.nombre_coop) 
        dataCreditos['mes_de_Pago'] = str(pagoCre.mes_de_Pago )
        dataCreditos['anio_de_pago'] = str(pagoCre.anio_de_pago)
        dataCreditos['fecha'] = pagoCre.fecha
        dataCreditos['valor'] = pagoCre.valor
        dataCreditos['id_caja'] = str(pagoCre.caja)
        dataCreditos['descripcion'] = pagoCre.descripcion
        dataCreditos['id_empresa'] = str(pagoCre.id_empresa)

        ListaPagoCreditos.append(dataCreditos)
    return JsonResponse({'ListaPagoCreditos':ListaPagoCreditos}, safe=False)

def resumenPagoCredito(request):

    return render(request, 'resumenPagoCredito.html')

def registroPagoDecimos(request):
    if request.method == 'GET':
        return render(request, 'registroPagoDecimos.html',{
            'form':form_pagoDecimos

        })
    else:
        form2 = form_pagoDecimos(request.POST)
        nuevoPagoDecimos = form2.save(commit=False)

        caja_reg_decimo = cajasReg.objects.get(usuario=request.user)

        nuevoPagoDecimos.caja = caja_reg_decimo
        nuevoPagoDecimos.usuario = request.user
        nuevoPagoDecimos.fecha = request.POST['fecha']
        nuevoPagoDecimos.save()

        return redirect('ResumenPagoDecimos')

def jsonPagoDecimos(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=0)
    caja_decimos = cajasReg.objects.get(usuario=request.user)
    decimosConsulta = decimos.objects.filter(fecha__range=[fecha_inicial,fecha_actual],caja=caja_decimos)
    ListaPagoDecimos = []
    for dec in decimosConsulta:
        dataDecimos = {}
        dataDecimos['id_empresa'] = str(dec.id_empresa)
        dataDecimos['caja'] = str(dec.caja)
        dataDecimos['colaborador'] = str(dec.colaborador)
        dataDecimos['valor'] = dec.valor
        dataDecimos['fecha'] = dec.fecha
        dataDecimos['descripcion'] = dec.descripcion

        ListaPagoDecimos.append(dataDecimos)
        
    return JsonResponse({'ListaPagoDecimos':ListaPagoDecimos},safe=False)

def resumenPagoDecimos(request):
    return render(request, 'resumenPagodecimos.html')

def registroPagoIess(request):
    if request.method == 'GET':
        return render(request, 'registroPagoIess.html',{
            'form':form_planillasIess
        })
    else:
        form2 = form_planillasIess(request.POST)
        nuevoPagoIess = form2.save(commit=False)

        caja_reg_iess = cajasReg.objects.get(usuario=request.user)
        nuevoPagoIess.caja = caja_reg_iess
        nuevoPagoIess.fecha = request.POST['fecha']
        nuevoPagoIess.save()

        return redirect('ResumenPagoIess')

def resumenPagoIess(request):
    return render(request, 'resumenPagoIess.html')

def jsonPagoIess(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=0)
    caja_Iess = cajasReg.objects.get(usuario=request.user)
    IessConsulta = planillasIESS.objects.filter(fecha__range=[fecha_inicial,fecha_actual],caja=caja_Iess)
    ListaPagoIess = []
    for pagoIess in IessConsulta:
        datai = {}
        datai['id_empresa'] = str(pagoIess.id_empresa)
        datai['caja'] = str(pagoIess.caja)
        datai['colaborador'] = str(pagoIess.colaborador)
        datai['valor'] = pagoIess.valor
        datai['fecha'] = pagoIess.fecha
        datai['descripcion'] = pagoIess.descripcion
        ListaPagoIess.append(datai)
    return JsonResponse({'ListaPagoIess':ListaPagoIess}, safe=False)