from django.shortcuts import render,redirect
from datetime import datetime, timedelta
from django.db.models import Sum
from .forms import form_registroInvRetiros, form_registroInvFacturas, form_registroSalidasInstalaciones
from .forms import form_precierre, form_salidaVentasContado, form_movimientosInventario,form_selecResumenInvFacturas
from .forms import  form_clientes_reg
from . models import ingresosRetiros, nuevo_usado, ingresoFacturas, salidaInstalaciones
from . models import codigo_prod, salidaVentasContado,  movimimientosInventario, cierreInventario2
from . models import bodega,clientes
from egresos.models import facturasProveedores
from general.models import empresa


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
        
        VTFactura = facturasProveedores.objects.get(id=request.POST['idFactura'])
        nuevoRegInv.precio_factura =VTFactura.valor
        #print(VTFactura.valor)
        #nue_usa = nuevo_usado.objects.get(estatus_uso = 'Nuevo')
        #print(nue_usa)
        #nuevoRegInv.idEstatusUso = nue_usa
        nuevoRegInv.fecha_ingreso = request.POST['fecha_ingreso']
        nuevoRegInv.save()
        

        return redirect('ResumenInvFacturas', request.POST['idFactura'])
    
def PreResumenInvFacturas(request):
    if request.method == "GET":
        ingresoInv = ingresoFacturas.objects.all()

        return render(request,'preResumenInventarioFacturas.html',{
            'ingresoInv':ingresoInv,
            'form':form_selecResumenInvFacturas,
        })
    else:
        print(request.POST['idFactura'])
        permiso = facturasProveedores.objects.get(id = request.POST['idFactura']).estadoEntrega
        return redirect('ResumenInvFacturas', request.POST['idFactura'])

    
def ResumenInvFacturas(request,idfactura):
    ingresoInv = ingresoFacturas.objects.filter(idFactura=idfactura)
    
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
        # se guarda la fecha de ingreso en la tabla de facturas
        ingresoInv = ingresoFacturas.objects.filter(idFactura=idfactura).first()
        factura.fechaentrega = ingresoInv.fecha_ingreso
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

def registroMovimientosInv(request):
    if request.method == 'GET':

        return render(request, 'registroMovimientosInv.html',{
            'form':form_movimientosInventario,
        })
    else:
        form2 = form_movimientosInventario(request.POST)
        nuevoregistro = form2.save(commit=False)
        nuevoregistro.digitador = request.user
        nuevoregistro.fecha = request.POST['fecha']
        nuevoregistro.save()
        return redirect('resumenMovimientosInv')
def resumenMovimientosInv(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=30)
    resumen_mov_inv =  movimimientosInventario.objects.filter(fecha__range=[fecha_inicial,fecha_actual])

    return render(request, 'resumenMovimientosInv.html',{
        'resumen_mov_inv':resumen_mov_inv,
    })


def preCierreInventario(request):
    if request.method == 'GET':
        return render(request, 'SeleccionCierre.html',{
            'form' : form_precierre,
        })
    else:
        #fecha_actual = datetime.now().date()
        fecha_formulario = request.POST['fecha']
        formato_str = "%Y-%m-%d"
        fecha_actual = datetime.strptime(fecha_formulario,formato_str) 
        fecha_actual=fecha_actual.date()
        equipos = codigo_prod.objects.all().exclude(seguimientoProducto=False)
        items_excluir = codigo_prod.objects.get(seguimientoProducto=False)
        uso = nuevo_usado.objects.all()
        ingresos_fact2 = ingresoFacturas.objects.filter(fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega']).exclude(idcodigo=items_excluir)
        ingresos_retiros_inv = ingresosRetiros.objects.filter(fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'])
        salida_instalaciones = salidaInstalaciones.objects.filter(fecha_instalacion = fecha_actual, idBodega = request.POST['idBodega'] )
        mov_entrada_inventario = movimimientosInventario.objects.filter(fecha=fecha_actual,idBodega_destino = request.POST['idBodega'] )
        mov_salida_inventario = movimimientosInventario.objects.filter(fecha=fecha_actual,idBodega_origen = request.POST['idBodega'] )
        
        salida_ventascontado = salidaVentasContado.objects.filter(fecha_venta = fecha_actual, idBodega=request.POST['idBodega'])
        totalesIngreFac = []
        totalesIngreRet = []
        totalesSalInstalaciones = []
        totalesSalidaVentasContado = []
        total_ingreso_movimiento_inv = []
        total_salida_movimiento_inv = []
        for i in equipos:
            for j in uso:
                total_ingreso_facturas = ingresoFacturas.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'] ).aggregate(total_ingreso_facturas=Sum('cantidad'))['total_ingreso_facturas']
                datat = {}
                datat['codigo']=i.codigo
                datat['uso']= j.estatus_uso
                datat['cantidad'] = total_ingreso_facturas
                if int(total_ingreso_facturas or 0) > 0:
                    totalesIngreFac.append(datat)

                ingreso_inv_mov = movimimientosInventario.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha = fecha_actual,idBodega_destino = request.POST['idBodega'] ).aggregate( ingreso_inv_mov=Sum('cantidad'))['ingreso_inv_mov']
                movin1 = {}
                movin1['codigo'] = i.codigo
                movin1['uso'] = j.estatus_uso
                movin1['cantidad'] = ingreso_inv_mov
                if int(ingreso_inv_mov or 0) > 0:
                    total_ingreso_movimiento_inv.append(movin1)

                salida_inv_mov = movimimientosInventario.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha = fecha_actual,idBodega_origen = request.POST['idBodega'] ).aggregate(salida_inv_mov=Sum('cantidad'))['salida_inv_mov']
                movout1 = {}
                movout1['codigo'] = i.codigo
                movout1['uso'] = j.estatus_uso
                movout1['cantidad'] = salida_inv_mov
                if int(salida_inv_mov or 0) > 0:
                    total_salida_movimiento_inv.append(movout1)



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

                total_salida_venta_contado = salidaVentasContado.objects.filter(idcodigo=i.id ,idEstatusUso=j.id, fecha_venta = fecha_actual, idBodega = request.POST['idBodega']).aggregate(total_salida_venta_contado=Sum('cantidad'))['total_salida_venta_contado']
             
                data4 = {}
                data4['codigo'] = i.codigo
                data4['cantidad'] = total_salida_venta_contado
                data4['uso'] = j.estatus_uso

                if int(total_salida_venta_contado or 0) > 0:
                    totalesSalidaVentasContado.append(data4)
                
            ## SUMA DE INGRESOS
        total_ingreso_inventario = []
        total_salida_inventario = []
        for i in equipos:
            for j in uso:
                total_ingresofac = ingresoFacturas.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'] ).aggregate(total_ingresofac=Sum('cantidad'))['total_ingresofac']
                total_ingresoret = ingresosRetiros.objects.filter(idcodigo=i.id, idEstatusUso= j.id,fecha_ingreso = fecha_actual, idBodega = request.POST['idBodega'] ).aggregate(total_ingresoret=Sum('cantidad'))['total_ingresoret']
                cantidad_total = int(total_ingresofac or 0) + int(total_ingresoret or 0)
                data5 = {}
                data5['codigo'] = i.codigo
                data5['cantidad'] = cantidad_total
                data5['uso'] = j.estatus_uso

                if cantidad_total > 0:
                    total_ingreso_inventario.append(data5)
                
                total_salida_inst = salidaInstalaciones.objects.filter(idcodigo=i.id,idEstatusUso=j.id, fecha_instalacion = fecha_actual,idBodega = request.POST['idBodega']).aggregate(total_salida_inst=Sum('cantidad'))['total_salida_inst']
                total_salida_venta_contado = salidaVentasContado.objects.filter(idcodigo=i.id ,idEstatusUso=j.id, fecha_venta = fecha_actual, idBodega = request.POST['idBodega']).aggregate(total_salida_venta_contado=Sum('cantidad'))['total_salida_venta_contado']
                cantidad_total_salida = int(total_salida_inst or 0) + (total_salida_venta_contado or 0)
                data6 = {}
                data6['codigo'] = i.codigo
                data6['cantidad'] = cantidad_total_salida
                data6['uso']=j.estatus_uso
                if cantidad_total_salida > 0:
                    total_salida_inventario.append(data6)

        fecha_ayer = fecha_actual - timedelta(days=1)
        cierreAnteriorInv = cierreInventario2.objects.filter(fecha=fecha_ayer,idBodega = request.POST['idBodega'])
        paasCierreInv = False
        if not cierreAnteriorInv.exists():
            paasCierreInv = False
        else:
            paasCierreInv = True

        return render(request, 'preCierre.html',{
            'idBodega':request.POST['idBodega'],
            'fecha':fecha_actual,
            'id_empresa':request.POST['id_empresa'],
            #'ingresoFacturasInv': ingresoFacturasInv,
            'ingresos_fact2': ingresos_fact2,
            'totalesIngreFac':totalesIngreFac,

            'ingresos_retiros_inv':ingresos_retiros_inv,
            'totalesIngreRet':totalesIngreRet,

            'total_ingreso_inventario':total_ingreso_inventario,

            'salida_instalaciones':salida_instalaciones,
            'totalesSalInstalaciones':totalesSalInstalaciones,

            'salida_ventascontado':salida_ventascontado,
            'totalesSalidaVentasContado': totalesSalidaVentasContado,
            'total_salida_inventario':total_salida_inventario,
            #movimientos
            'mov_entrada_inventario':mov_entrada_inventario,
            'mov_salida_inventario':mov_salida_inventario,
            'total_ingreso_movimiento_inv':total_ingreso_movimiento_inv,
            'total_salida_movimiento_inv':total_salida_movimiento_inv,
            #amterior
            'cierreAnteriorInv':cierreAnteriorInv,
            #pass Cierre
            #Pass cierre
            'paasCierreInv':paasCierreInv,
        })
    
def cierreInventarioBodega(request, idBodega, fecha, id_empresa):
    if request.method  == 'GET':
        formato_str = "%Y-%m-%d"
        #fecha_ayer = datetime.strptime(fecha_consulta,formato_str) - timedelta(days=1)
        fecha = datetime.strptime(fecha,formato_str)
 
        fecha = fecha.date()

        equipos2 = codigo_prod.objects.all()
        uso2 = nuevo_usado.objects.all()

        totalesIngreFac = []
        totalesIngreRet = []
        totalesSalInstalaciones = []
        totalesSalidaVentasContado = []
        total_ingreso_movimiento_inv = []
        total_salida_movimiento_inv = []

        for i in equipos2:
            for j in uso2:

                ingreso_inv_mov = movimimientosInventario.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha = fecha, idBodega_destino = idBodega).aggregate( ingreso_inv_mov=Sum('cantidad'))['ingreso_inv_mov']
                movin1 = {}
                movin1['codigo'] = i.codigo
                movin1['uso'] = j.estatus_uso
                movin1['cantidad'] = ingreso_inv_mov
                if int(ingreso_inv_mov or 0) > 0:
                    total_ingreso_movimiento_inv.append(movin1)

                salida_inv_mov = movimimientosInventario.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha = fecha ,idBodega_origen = idBodega ).aggregate(salida_inv_mov=Sum('cantidad'))['salida_inv_mov']
                movout1 = {}
                movout1['codigo'] = i.codigo
                movout1['uso'] = j.estatus_uso
                movout1['cantidad'] = salida_inv_mov
                if int(salida_inv_mov or 0) > 0:
                    total_salida_movimiento_inv.append(movout1)

                total_ingreso_retiros = ingresosRetiros.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha_ingreso=fecha, idBodega = idBodega ).aggregate(total_ingreso_retiros=Sum('cantidad'))['total_ingreso_retiros']
                data2 = {}
                data2['codigo']=i.codigo
                data2['uso']=j.estatus_uso
                data2['cantidad'] = total_ingreso_retiros
               

                if int(total_ingreso_retiros or 0) > 0:
                    totalesIngreRet.append(data2)

                total_ingreso_facturas = ingresoFacturas.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha_ingreso = fecha, idBodega = idBodega ).aggregate(total_ingreso_facturas=Sum('cantidad'))['total_ingreso_facturas']
            
                datat = {}
                datat['codigo']=i.codigo
                datat['uso']= j.estatus_uso
                datat['cantidad'] = total_ingreso_facturas
                if int(total_ingreso_facturas or 0) > 0:
                    totalesIngreFac.append(datat)
                
                total_salida_inst = salidaInstalaciones.objects.filter(idcodigo=i.id,idEstatusUso=j.id, fecha_instalacion = fecha,idBodega = idBodega).aggregate(total_salida_inst=Sum('cantidad'))['total_salida_inst']
                data3 = {}
                data3['codigo'] = i.codigo
                data3['cantidad'] = total_salida_inst
                data3['uso']=j.estatus_uso

                if int(total_salida_inst or 0) > 0:
                    totalesSalInstalaciones.append(data3)

                total_salida_venta_contado = salidaVentasContado.objects.filter(idcodigo=i.id ,idEstatusUso=j.id, fecha_venta = fecha, idBodega = idBodega).aggregate(total_salida_venta_contado=Sum('cantidad'))['total_salida_venta_contado']
              
                data4 = {}
                data4['codigo'] = i.codigo
                data4['cantidad'] = total_salida_venta_contado
                data4['uso'] = j.estatus_uso

                if int(total_salida_venta_contado or 0) > 0:
                    totalesSalidaVentasContado.append(data4)
                
            total_ingreso_inventario = []
            total_salida_inventario = []
            #total_ingreso_movimiento_inv = []
            #total_salida_movimiento_inv = []
            for i in equipos2:
                for j in uso2:
                    total_ingresofac = ingresoFacturas.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha_ingreso = fecha, idBodega = idBodega ).aggregate(total_ingresofac=Sum('cantidad'))['total_ingresofac']
                    total_ingresoret = ingresosRetiros.objects.filter(idcodigo=i.id, idEstatusUso= j.id,fecha_ingreso = fecha, idBodega = idBodega ).aggregate(total_ingresoret=Sum('cantidad'))['total_ingresoret']
                    cantidad_total = int(total_ingresofac or 0) + int(total_ingresoret or 0)
                    data5 = {}
                    data5['codigo'] = i.codigo
                    data5['cantidad'] = cantidad_total
                    data5['uso'] = j.estatus_uso

                    if cantidad_total > 0:
                        total_ingreso_inventario.append(data5)
                        
                    total_salida_inst = salidaInstalaciones.objects.filter(idcodigo=i.id,idEstatusUso=j.id, fecha_instalacion = fecha,idBodega = idBodega).aggregate(total_salida_inst=Sum('cantidad'))['total_salida_inst']
                    total_salida_venta_contado = salidaVentasContado.objects.filter(idcodigo=i.id ,idEstatusUso=j.id, fecha_venta = fecha, idBodega = idBodega).aggregate(total_salida_venta_contado=Sum('cantidad'))['total_salida_venta_contado']
                    cantidad_total_salida = int(total_salida_inst or 0) + (total_salida_venta_contado or 0)
                    data6 = {}
                    data6['codigo'] = i.codigo
                    data6['cantidad'] = int(cantidad_total_salida or 0)
                    data6['uso']=j.estatus_uso
                    if cantidad_total_salida > 0:
                        total_salida_inventario.append(data6)
                    

     
        fecha_ayer = fecha - timedelta(days=1)
        cierreAnteriorInv = cierreInventario2.objects.filter(fecha=fecha_ayer,idBodega = idBodega)
        #lista_cierreAnterior = []
        #for ii in cierreAnteriorInv:
        #    tempoList = {}
        #    tempoList['codigo'] = str(ii.idcodigo)
        #    tempoList['uso'] = str(ii.idEstatusUso).strip()
        #    tempoList['cantidad']= int(ii.cantidad or 0)
        #    lista_cierreAnterior.append(tempoList)
      


        inventario = {}
        for item in total_ingreso_inventario:
            clave = (item['codigo'], item['uso'])
            cantidad = item["cantidad"]
            inventario[clave] = inventario.get(clave, 0) + cantidad

        for item in total_salida_inventario:
            clave = (item['codigo'], item['uso'])
            cantidad = item['cantidad']
            inventario[clave] = inventario.get(clave, 0) - cantidad

        for item in total_ingreso_movimiento_inv:
            clave = (item['codigo'], item['uso'])
            cantidad = item['cantidad']
            inventario[clave] = inventario.get(clave, 0) + cantidad

        for item in total_salida_movimiento_inv :
            clave = (item['codigo'], item['uso'])
            cantidad = item['cantidad']
            inventario[clave] = inventario.get(clave, 0) - cantidad


        for item in cierreAnteriorInv:
            clave = (str(item.idcodigo).strip(),str(item.idEstatusUso).strip())
            cantidad = int(item.cantidad or 0)
            inventario[clave] = inventario.get(clave, 0) + cantidad
        

        resultados = [{'codigo': codigo, 'uso': uso, 'cantidad': cantidad} for (codigo, uso), cantidad in inventario.items()]
                

        return render (request, 'RegistroCierreInventarioBod.html',{
            'totalesIngreFac':totalesIngreFac,
            'totalesIngreRet':totalesIngreRet,
            'total_ingreso_inventario':total_ingreso_inventario,

            'totalesSalInstalaciones':totalesSalInstalaciones,
            'totalesSalidaVentasContado':totalesSalidaVentasContado,
            'total_salida_inventario':total_salida_inventario,
            'resultados':resultados,
            'total_ingreso_movimiento_inv':total_ingreso_movimiento_inv,
            'total_salida_movimiento_inv': total_salida_movimiento_inv,
            #anterior
            'cierreAnteriorInv':cierreAnteriorInv,

            
        })
    else:

        equipos2 = codigo_prod.objects.all()
        uso2 = nuevo_usado.objects.all()

        totalesIngreFac = []
        totalesIngreRet = []
        totalesSalInstalaciones = []
        totalesSalidaVentasContado = []
        total_ingreso_movimiento_inv = []
        total_salida_movimiento_inv = []

        for i in equipos2:
            for j in uso2:

                ingreso_inv_mov = movimimientosInventario.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha = fecha,idBodega_destino = idBodega).aggregate( ingreso_inv_mov=Sum('cantidad'))['ingreso_inv_mov']
                movin1 = {}
                movin1['codigo'] = i.codigo
                movin1['uso'] = j.estatus_uso
                movin1['cantidad'] = ingreso_inv_mov
                if int(ingreso_inv_mov or 0) > 0:
                    total_ingreso_movimiento_inv.append(movin1)

                salida_inv_mov = movimimientosInventario.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha = fecha ,idBodega_origen = idBodega ).aggregate(salida_inv_mov=Sum('cantidad'))['salida_inv_mov']
                movout1 = {}
                movout1['codigo'] = i.codigo
                movout1['uso'] = j.estatus_uso
                movout1['cantidad'] = salida_inv_mov
                if int(salida_inv_mov or 0) > 0:
                    total_salida_movimiento_inv.append(movout1)

                total_ingreso_retiros = ingresosRetiros.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha_ingreso=fecha, idBodega = idBodega ).aggregate(total_ingreso_retiros=Sum('cantidad'))['total_ingreso_retiros']
                data2 = {}
                data2['codigo']=i.codigo
                data2['uso']=j.estatus_uso
                data2['cantidad'] = total_ingreso_retiros
                #print(data2)

                if int(total_ingreso_retiros or 0) > 0:
                    totalesIngreRet.append(data2)

                total_ingreso_facturas = ingresoFacturas.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha_ingreso = fecha, idBodega = idBodega ).aggregate(total_ingreso_facturas=Sum('cantidad'))['total_ingreso_facturas']
            
                datat = {}
                datat['codigo']=i.codigo
                datat['uso']= j.estatus_uso
                datat['cantidad'] = total_ingreso_facturas
                if int(total_ingreso_facturas or 0) > 0:
                    totalesIngreFac.append(datat)
                
                total_salida_inst = salidaInstalaciones.objects.filter(idcodigo=i.id,idEstatusUso=j.id, fecha_instalacion = fecha,idBodega = idBodega).aggregate(total_salida_inst=Sum('cantidad'))['total_salida_inst']
                data3 = {}
                data3['codigo'] = i.codigo
                data3['cantidad'] = total_salida_inst
                data3['uso']=j.estatus_uso

                if int(total_salida_inst or 0) > 0:
                    totalesSalInstalaciones.append(data3)

                total_salida_venta_contado = salidaVentasContado.objects.filter(idcodigo=i.id ,idEstatusUso=j.id, fecha_venta = fecha, idBodega = idBodega).aggregate(total_salida_venta_contado=Sum('cantidad'))['total_salida_venta_contado']
                #print(total_salida_venta_contado)
                data4 = {}
                data4['codigo'] = i.codigo
                data4['cantidad'] = total_salida_venta_contado
                data4['uso'] = j.estatus_uso

                if int(total_salida_venta_contado or 0) > 0:
                    totalesSalidaVentasContado.append(data4)
                
            total_ingreso_inventario = []
            total_salida_inventario = []
            #total_ingreso_movimiento_inv = []
            #total_salida_movimiento_inv = []
            for i in equipos2:
                for j in uso2:
                    total_ingresofac = ingresoFacturas.objects.filter(idcodigo=i.id, idEstatusUso= j.id, fecha_ingreso = fecha, idBodega = idBodega ).aggregate(total_ingresofac=Sum('cantidad'))['total_ingresofac']
                    total_ingresoret = ingresosRetiros.objects.filter(idcodigo=i.id, idEstatusUso= j.id,fecha_ingreso = fecha, idBodega = idBodega ).aggregate(total_ingresoret=Sum('cantidad'))['total_ingresoret']
                    cantidad_total = int(total_ingresofac or 0) + int(total_ingresoret or 0)
                    data5 = {}
                    data5['codigo'] = i.codigo
                    data5['cantidad'] = cantidad_total
                    data5['uso'] = j.estatus_uso

                    if cantidad_total > 0:
                        total_ingreso_inventario.append(data5)
                        
                    total_salida_inst = salidaInstalaciones.objects.filter(idcodigo=i.id,idEstatusUso=j.id, fecha_instalacion = fecha, idBodega = idBodega).aggregate(total_salida_inst=Sum('cantidad'))['total_salida_inst']
                    total_salida_venta_contado = salidaVentasContado.objects.filter(idcodigo=i.id ,idEstatusUso=j.id, fecha_venta = fecha, idBodega = idBodega).aggregate(total_salida_venta_contado=Sum('cantidad'))['total_salida_venta_contado']
                    cantidad_total_salida = int(total_salida_inst or 0) + (total_salida_venta_contado or 0)
                    data6 = {}
                    data6['codigo'] = i.codigo
                    data6['cantidad'] = int(cantidad_total_salida or 0)
                    data6['uso']=j.estatus_uso
                    if cantidad_total_salida > 0:
                        total_salida_inventario.append(data6)
        
        formato_str = "%Y-%m-%d"
        #fecha_ayer = datetime.strptime(fecha_consulta,formato_str) - timedelta(days=1)
        fecha = datetime.strptime(fecha,formato_str)
 
        fecha = fecha.date()
             
        fecha_ayer = fecha - timedelta(days=1)
        cierreAnteriorInv = cierreInventario2.objects.filter(fecha=fecha_ayer, idBodega = idBodega)

       
        inventario = {}
        for item in total_ingreso_inventario:
            clave = (item["codigo"], item["uso"])
            cantidad = item["cantidad"]
            inventario[clave] = inventario.get(clave, 0) + cantidad

        for item in total_salida_inventario:
            clave = (item["codigo"], item["uso"])
            cantidad = item["cantidad"]
            inventario[clave] = inventario.get(clave, 0) - cantidad

        for item in total_ingreso_movimiento_inv:
            clave = (item["codigo"], item["uso"])
            cantidad = item["cantidad"]
            inventario[clave] = inventario.get(clave, 0) + cantidad

        for item in total_salida_movimiento_inv :
            clave = (item["codigo"], item["uso"])
            cantidad = item["cantidad"]
            inventario[clave] = inventario.get(clave, 0) - cantidad
        
        for item in cierreAnteriorInv:
            clave = (str(item.idcodigo).strip(),str(item.idEstatusUso).strip())
            print(clave)
            cantidad = item.cantidad
            inventario[clave] = inventario.get(clave, 0) + cantidad

        resultados = [{'codigo': codigo, 'uso': uso, 'cantidad': cantidad} for (codigo, uso), cantidad in inventario.items()]
       
        for tempo in resultados:
            empre_tempo = empresa.objects.get(id=id_empresa)
            bodega_tempo = bodega.objects.get(id=idBodega)
            codigo_tempo = codigo_prod.objects.get(codigo=tempo['codigo'])
            uso_tempo = nuevo_usado.objects.get(estatus_uso= tempo['uso'])
            nuevoReg = cierreInventario2(id_empresa= empre_tempo, idBodega=bodega_tempo, idcodigo = codigo_tempo, idEstatusUso = uso_tempo,cantidad =tempo['cantidad'], digitador = request.user, fecha = fecha, observacion =request.POST['observacion'])
            nuevoReg.save()
         
        return redirect('ResumenCierreInventarioBodega')
    
def ResumenCierreInventarioBodega(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=90)
    cierresInventario = cierreInventario2.objects.filter(fecha__range=[fecha_inicial,fecha_actual]).order_by('-fecha')
    return render(request,'ResumenCierreInventarioBod.html',{
        'cierresInventario':cierresInventario,
    })

def RegistroClientes(request):
    if request.method == 'GET':
        return render(request,'registroClientes.html',{
            'form':form_clientes_reg,
        })
    else:
        form2 = form_clientes_reg(request.POST)
        nuevoregistro = form2.save(commit=False)
        nuevoregistro.save()
       
        return redirect('ResumenClientes')
def ResumenClientes(request):
    clientesList = clientes.objects.all()
    return render(request,'listadoClientes.html',{
        'clientesList':clientesList,
    })

def actualizacionFacturas(request):
    #act = facturasProveedores.objects.all()
    #for item in act:
    #    item.estadoEntrega =True
    #    item.save()
    return render(request,'actualizacionfacturas.html')

