from django.shortcuts import render,redirect
from datetime import datetime, timedelta
from django.db.models import Sum
from .forms import form_registroInvRetiros, form_registroInvFacturas, form_registroSalidasInstalaciones
from .forms import form_precierre, form_salidaVentasContado
from . models import ingresosRetiros, nuevo_usado, ingresoFacturas, salidaInstalaciones
from . models import codigo_prod, salidaVentasContado
from egresos.models import facturasProveedores


# Create your views here.

def homeInventario(request):
    return render (request, 'home_inventario.html')

def ingresosInvRetiros(request):
    if request.method == 'GET':
        return render(request, 'RegistroInvRetiros.html',{
            'form': form_registroInvRetiros,
        })
    else:
        form2 = form_registroInvRetiros(request.POST)
        nuevoRegInv = form2.save(commit=False)

        nuevoRegInv.id_usuario = request.user
        nuevoRegInv.fecha_ingreso = request.POST['fecha_ingreso']
        nuevoRegInv.save()
        return redirect('ResumenIngInvRetiros')
    
def ResumenIngInvRetiros(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=30)
    ingresoInv = ingresosRetiros.objects.filter(fecha_ingreso__range=[fecha_inicial,fecha_actual])
    return render(request, 'ResumenRegistroInvRetiros.html',{
        'ingresoInv' : ingresoInv,
    })

def ingresosInvFacturas(request):
    if request.method == 'GET':
        return render(request, 'RegistroInvFacturas.html',{
            'form': form_registroInvFacturas,
        })
    else:
        form2 = form_registroInvFacturas(request.POST)
        nuevoRegInv = form2.save(commit=False)
        nuevoRegInv.id_usuario = request.user
        nuevoRegInv.estadoIngreso = False#
        #print(request.POST['idFactura'])
        VTFactura = facturasProveedores.objects.get(id=request.POST['idFactura'])
        nuevoRegInv.precio_factura = VTFactura.valor
        #print(VTFactura.valor)
        #nue_usa = nuevo_usado.objects.get(estatus_uso = 'Nuevo')
        #print(nue_usa)
        #nuevoRegInv.idEstatusUso = nue_usa
        nuevoRegInv.fecha_ingreso = request.POST['fecha_ingreso']
        nuevoRegInv.save()

        return redirect('ResumenInvFacturas', request.POST['idFactura'])
    
def ResumenInvFacturas(request,idfactura):
    ingresoInv = ingresoFacturas.objects.filter(idFactura=idfactura)
    print(ingresoInv)
    total_calculado = 0
    for i in ingresoInv:
        subtotal = float(i.cantidad*i.precio_in)*(1.12)
        total_calculado = total_calculado + subtotal
    total_calculado = round(total_calculado, 3)

    vtotalfactura = facturasProveedores.objects.get(id=idfactura)
    if request.method == 'GET':
        return render(request, 'ResumenRegistroInvFacturas.html',{
            'ingresoInv':ingresoInv,
            'total_calculado':total_calculado,
            'total_factura':vtotalfactura.valor,
        })
    else:
        factura = facturasProveedores.objects.get(id=idfactura)
        factura.estadoEntrega = True
        factura.save()
        return redirect('homeInventario')


def ResgistroSalidaInstalacion(request):
    if request.method == 'GET':
        return render(request, 'registroSalidaInsta.html',{
            'form': form_registroSalidasInstalaciones,
        })
    else:
        form2 = form_registroSalidasInstalaciones(request.POST)
        nuevoregistro = form2.save(commit=False)
        nuevoregistro.id_usuario = request.user
        nuevoregistro.fecha_instalacion = request.POST['fecha_instalacion']
        nuevoregistro.save()
        return redirect('ResumenSalidaInstalacion')
    
def ResumenSalidaInstalacion(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=30)
    SalidaIns = salidaInstalaciones.objects.filter(fecha_instalacion__range=[fecha_inicial,fecha_actual])
    return render(request,'ResumenSalidaInstalaciones.html',{
        'SalidaIns':SalidaIns,
    })
def RegistroSalidaVentasContado(request):
    if request.method == 'GET':
        return render(request, 'RegistroSalidaVentasContado.html',{
            'form': form_salidaVentasContado,
        })
    else:
        form2 = form_salidaVentasContado(request.POST)
        nuevoregistro = form2.save(commit=False)

        nuevoregistro.id_usuario = request.user
        nuevoregistro.fecha_venta = request.POST['fecha_venta']
        nuevoregistro.fecha_entrega = request.POST['fecha_entrega']
        nuevoregistro.save()
        return redirect('ResumenSalidaVentasContado')

def ResumenSalidaVentasContado(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=30)
    salidacontado = salidaVentasContado.objects.filter(fecha_entrega__range=[fecha_inicial,fecha_actual])
    return render(request, 'ResumenSalidaVentasContado.html',{
        'salidacontado':salidacontado,
    })



def preCierreInventario(request):
    if request.method == 'GET':
        return render(request, 'SeleccionCierre.html',{
            'form' : form_precierre,
        })
    else:
        fecha_actual = datetime.now().date()
        equipos = codigo_prod.objects.all()
        uso = nuevo_usado.objects.all()
        ingresos_fact2 = ingresoFacturas.objects.filter(fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'])
        ingresos_retiros_inv = ingresosRetiros.objects.filter(fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'])
        salida_instalaciones = salidaInstalaciones.objects.filter(fecha_instalacion = fecha_actual, idBodega = request.POST['idBodega'] )
        salida_ventascontado = salidaVentasContado.objects.filter(fecha_venta = fecha_actual, idBodega=request.POST['idBodega'])
        totalesIngreFac = []
        #estadoFacturas = nuevo_usado.objects.get(estatus_uso = 'Nuevo')
        #for i in equipos:
            #ingresos_fact = ingresoFacturas.objects.filter(idcodigo=i.id,fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'])
         #   total_ingreso = ingresoFacturas.objects.filter(idcodigo=i.id, fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'] ).aggregate(total_ingreso=Sum('cantidad'))['total_ingreso']
         #  print(total_ingreso)
         #   datat = {}
         #   datat['codigo']=i.codigo
         #   datat['uso']= estadoFacturas
         #   datat['cantidad'] = total_ingreso
         #   if int(total_ingreso or 0) > 0:
         #      totalesIngreFac.append(datat)

            #for j in ingresos_fact:
            #    data = {}
            #    data['idcodigo']=j.idcodigo
            #    data['cantidad']=j.cantidad
            #    data['idEstatusUso']=j.idEstatusUso
            #    ingresoFacturasInv.append(data)
        totalesIngreRet = []
        totalesSalInstalaciones = []
        for i in equipos:
            for j in uso:
                total_ingreso_facturas = ingresoFacturas.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'] ).aggregate(total_ingreso_facturas=Sum('cantidad'))['total_ingreso_facturas']
            
                datat = {}
                datat['codigo']=i.codigo
                datat['uso']= j.estatus_uso
                datat['cantidad'] = total_ingreso_facturas
                if int(total_ingreso_facturas or 0) > 0:
                    totalesIngreFac.append(datat)




                total_ingreso = ingresosRetiros.objects.filter(idcodigo=i.id, idEstatusUso= j.id,fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'] ).aggregate(total_ingreso=Sum('cantidad'))['total_ingreso']
                data2 = {}
                data2['codigo']=i.codigo
                data2['uso']=j.estatus_uso
                data2['cantidad'] = total_ingreso
                
                if int(total_ingreso or 0) > 0:
                    totalesIngreRet.append(data2)

                total_salida_inst = salidaInstalaciones.objects.filter(idcodigo=i.id,idEstatusUso=j.id, fecha_instalacion = fecha_actual,idBodega = request.POST['idBodega']).aggregate(total_salida_inst=Sum('cantidad'))['total_salida_inst']
                data3 = {}
                data3['codigo'] = i.codigo
                data3['cantidad'] = total_salida_inst
                data3['uso']=j.estatus_uso

                if int(total_salida_inst or 0) > 0:
                    totalesSalInstalaciones.append(data3)

                
            ## SUMA DE INGRESOS
        total_ingreso_inventario = []
        for i in equipos:
            for j in uso:
                total_ingresofac = ingresoFacturas.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'] ).aggregate(total_ingresofac=Sum('cantidad'))['total_ingresofac']
                total_ingresoret = ingresosRetiros.objects.filter(idcodigo=i.id, idEstatusUso= j.id,fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'] ).aggregate(total_ingresoret=Sum('cantidad'))['total_ingresoret']
                cantidad_total = int(total_ingresofac or 0) + int(total_ingresoret or 0)
                data4 = {}
                data4['codigo'] = i.codigo
                data4['cantidad'] = cantidad_total
                data4['uso'] = j.estatus_uso

                if cantidad_total > 0:
                    total_ingreso_inventario.append(data4)

        return render(request, 'preCierre.html',{
            #'ingresoFacturasInv': ingresoFacturasInv,
            'ingresos_fact2': ingresos_fact2,
            'totalesIngreFac':totalesIngreFac,

            'ingresos_retiros_inv':ingresos_retiros_inv,
            'totalesIngreRet':totalesIngreRet,

            'total_ingreso_inventario':total_ingreso_inventario,

            'salida_instalaciones':salida_instalaciones,
            'totalesSalInstalaciones':totalesSalInstalaciones,

            'salida_ventascontado':salida_ventascontado,
        })