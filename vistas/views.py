from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . forms import form_seleccion_caja_empresa, form_caja_empresa_cierre, form_cierres
from ingresos.models import ingresosCajas
from egresos.models import facturasProveedores, pagoColaboradores, planillasIESS, decimos
from egresos.models import pagoServicios, pagoCreditos
from movimientos.models import movimientos
from cierres.models import CierresCajas

from general.models import empresa, cajasReg
from cierres.models import CierresCajas


from datetime import datetime, timedelta
# Create your views here.

def selec_caja_empresa(request):

    if request.method == 'GET':
        return render(request, 'selec_caja_empresa.html',{
        'form': form_seleccion_caja_empresa
        })
    else:

        fecha_actual = datetime.now().date()
        fecha_inicial = fecha_actual - timedelta(days=7)
        #ingresos_dia = ingresosCajas.objects.filter(nombreCaja=request.POST['caja_selec'],empresaIngreso=request.POST['empresa_selec']).order_by('-fecha')
        ingresos_dia = ingresosCajas.objects.filter(nombreCaja=request.POST['caja_selec'],empresaIngreso=request.POST['empresa_selec'],fecha__range=[fecha_inicial,fecha_actual]).order_by('-fecha')
        egre_facturas = facturasProveedores.objects.filter(id_caja=request.POST['caja_selec'],id_empresa=request.POST['empresa_selec'],fechapago__range=[fecha_inicial,fecha_actual]).order_by('-fechafactura')
        egre_colaboradores = pagoColaboradores.objects.filter(id_caja=request.POST['caja_selec'],id_empresa=request.POST['empresa_selec'],fecha_pago__range=[fecha_inicial,fecha_actual]).order_by('-fecha_pago')
        egre_iess = planillasIESS.objects.filter(caja=request.POST['caja_selec'],id_empresa=request.POST['empresa_selec'],fecha__range=[fecha_inicial,fecha_actual]).order_by('-fecha')
        egre_decimos = decimos.objects.filter(caja=request.POST['caja_selec'],id_empresa=request.POST['empresa_selec'],fecha__range=[fecha_inicial,fecha_actual]).order_by('-fecha')
        egre_servicios = pagoServicios.objects.filter(caja=request.POST['caja_selec'],empresa_nuestra=request.POST['empresa_selec'],fecha__range=[fecha_inicial,fecha_actual]).order_by('-fecha')
        egre_creditos = pagoCreditos.objects.filter(caja=request.POST['caja_selec'],id_empresa=request.POST['empresa_selec'],fecha__range=[fecha_inicial,fecha_actual]).order_by('-fecha')
        mov_movimientos = movimientos.objects.filter(caja_origen_id=request.POST['caja_selec'],empresaCaja=request.POST['empresa_selec'],fecha__range=[fecha_inicial,fecha_actual]).order_by('-fecha')
        print(mov_movimientos)
        return render(request, 'selec_caja_empresa.html',{
        'form': form_seleccion_caja_empresa,
        'ingresos':ingresos_dia,
        'egrefac':egre_facturas,
        'egrecolaboradores':egre_colaboradores,
        'egre_iess':egre_iess,
        'egre_decimos':egre_decimos,
        'egre_servicios':egre_servicios,
        'egre_creditos':egre_creditos,
        'mov_movimientos':mov_movimientos,
  
        })
    

def cierresDiarios(request):
    if request.method == 'GET':
        fecha_consulta = datetime.now()
        cajau = cajasReg.objects.filter(usuario=request.user)
        cajaid = cajau[0].id

        ingresos_dia = ingresosCajas.objects.filter(nombreCaja=cajaid,fecha=fecha_consulta)
        egre_facturas = facturasProveedores.objects.filter(id_caja=cajaid,fechapago=fecha_consulta)
        egre_colaboradores = pagoColaboradores.objects.filter(id_caja=cajaid,fecha_pago=fecha_consulta)
        egre_iess = planillasIESS.objects.filter(caja=cajaid, fecha=fecha_consulta)
        egre_decimos = decimos.objects.filter(caja=cajaid, fecha=fecha_consulta)
        egre_servicios = pagoServicios.objects.filter(caja=cajaid, fecha=fecha_consulta)
        egre_creditos = pagoCreditos.objects.filter(caja=cajaid,fecha=fecha_consulta)
        mov_movimientos_salida = movimientos.objects.filter(caja_origen_id=cajaid,fecha=fecha_consulta)
        mov_movimientos_ingreso = movimientos.objects.filter(caja_destino_id=cajaid, fecha=fecha_consulta)
        cierreAnterior = CierresCajas.objects.filter(caja=cajaid, fecha=fecha_consulta )

        valorTotalIngresos = 0
        for ing_dia in ingresos_dia:
            valorTotalIngresos = ing_dia.valorIngreso + valorTotalIngresos
        
        valorTotalFacturas = 0
        for egresosEnFacturas in egre_facturas:
            valorTotalFacturas = valorTotalFacturas + egresosEnFacturas.valor

        valorTotalColaboradores = 0
        for egresosPagocolaboradores in egre_colaboradores:
            valorTotalColaboradores = valorTotalColaboradores + egresosPagocolaboradores.valor

        valorTotalPlanillasIees = 0
        for egresosPlanillasIees in egre_iess:
            valorTotalPlanillasIees = valorTotalPlanillasIees + egresosPlanillasIees.valor

        valorTotalDecinos = 0
        for egresosPagoDecimos in egre_decimos:
            valorTotalDecinos = valorTotalDecinos + egresosPagoDecimos.valor
    
        valorTotalServicios = 0
        for egrePagoServicios in egre_servicios:
            valorTotalServicios = valorTotalServicios + egrePagoServicios.valor

        valorTotalCreditos = 0
        for egresosPagoCreditos in egre_creditos:
            valorTotalCreditos = valorTotalCreditos + egresosPagoCreditos.valor
        
        valorTotalMovimientosIngreso = 0
        for TotalMovimientosIngreso in mov_movimientos_ingreso:
            valorTotalMovimientosIngreso = valorTotalMovimientosIngreso + TotalMovimientosIngreso.valor

        valorTotalMovimientosSalida = 0
        for TotalMovimientosSalida in mov_movimientos_salida:
            valorTotalMovimientosSalida = valorTotalMovimientosSalida + TotalMovimientosSalida.valor

        valor_cierre_anterior = 0
        for valor in cierreAnterior:
            valor_cierre_anterior = valor_cierre_anterior + valor.valorCierreActual

        valorTotalEgresosSis = valorTotalFacturas + valorTotalColaboradores + valorTotalPlanillasIees + valorTotalDecinos + valorTotalServicios + valorTotalCreditos
        valorTotalDia = valorTotalIngresos - valorTotalEgresosSis + valorTotalMovimientosIngreso - valorTotalMovimientosSalida
        valor_cierre_dia = valorTotalDia + valor_cierre_anterior
        return render(request, 'cierre_caja_empresa.html',{
            'form': form_caja_empresa_cierre,
            'ingresos':ingresos_dia,
            'egrefac':egre_facturas,
            'egrecolaboradores':egre_colaboradores,
            'egre_iess':egre_iess,
            'egre_decimos':egre_decimos,
            'egre_servicios':egre_servicios,
            'egre_creditos':egre_creditos,
            'mov_movimientos_salida':mov_movimientos_salida,
            'mov_movimientos_ingreso':mov_movimientos_ingreso,

            'valorTotalIngresos':valorTotalIngresos,
            'valorTotalFacturas' : valorTotalFacturas,
            'valorTotalColaboradores' : valorTotalColaboradores,
            'valorTotalPlanillasIees' : valorTotalPlanillasIees,
            'valorTotalDecinos':valorTotalDecinos,
            'valorTotalServicios':valorTotalServicios,
            'valorTotalCreditos':valorTotalCreditos,
            'valorTotalMovimientosIngreso':valorTotalMovimientosIngreso,
            'valorTotalMovimientosSalida': valorTotalMovimientosSalida,

            'valorTotalEgresosSis':valorTotalEgresosSis,
            'valorTotalDia':valorTotalDia,
            'valor_cierre_anterior':valor_cierre_anterior,
            'valor_cierre_dia':valor_cierre_dia ,


        })
    else:
        caja_cierre = cajasReg.objects.get(usuario=request.user)
        fecha_filtro = request.POST['fecha']
        #ingresos_dia = ingresosCajas.objects.filter(nombreCaja=request.POST['caja_selec'],empresaIngreso=request.POST['empresa_selec']).order_by('-fecha')
        ingresos_dia = ingresosCajas.objects.filter(nombreCaja=caja_cierre ,empresaIngreso=request.POST['empresa_selec'],fecha=fecha_filtro)
        egre_facturas = facturasProveedores.objects.filter(id_caja=caja_cierre ,id_empresa=request.POST['empresa_selec'],fechapago=fecha_filtro)
        egre_colaboradores = pagoColaboradores.objects.filter(id_caja=caja_cierre ,id_empresa=request.POST['empresa_selec'],fecha_pago=fecha_filtro)
        egre_iess = planillasIESS.objects.filter(caja=caja_cierre ,id_empresa=request.POST['empresa_selec'], fecha=fecha_filtro)
        egre_decimos = decimos.objects.filter(caja=caja_cierre ,id_empresa=request.POST['empresa_selec'], fecha=fecha_filtro)
        egre_servicios = pagoServicios.objects.filter(caja=caja_cierre ,empresa_nuestra=request.POST['empresa_selec'], fecha=fecha_filtro)
        egre_creditos = pagoCreditos.objects.filter(caja=caja_cierre ,id_empresa=request.POST['empresa_selec'], fecha=fecha_filtro)
        mov_movimientos = movimientos.objects.filter(caja_origen_id=caja_cierre ,empresaCaja=request.POST['empresa_selec'], fecha=fecha_filtro)
        mov_movimientos_salida = movimientos.objects.filter(caja_origen_id=caja_cierre,empresaCaja=request.POST['empresa_selec'],fecha=fecha_filtro)
        mov_movimientos_ingreso = movimientos.objects.filter(caja_destino_id=caja_cierre,empresaCaja=request.POST['empresa_selec'], fecha=fecha_filtro)
        print("*******")
        print(mov_movimientos_ingreso)
        formato_str = "%Y-%m-%d"
       #fecha_ayer = datetime.strptime(fecha_consulta,formato_str) - timedelta(days=1)
        fecha_ayer = datetime.strptime(fecha_filtro,formato_str) - timedelta(days=1)
        empresaCierre = empresa.objects.get(id=request.POST['empresa_selec'])
        cajaCierre = cajasReg.objects.get(id=caja_cierre.id)

        cierre_realizado = CierresCajas.objects.filter(empresa=empresaCierre, caja=cajaCierre, fecha=fecha_ayer)
    
        passCierre = False
        if not cierre_realizado.exists():
            print("no existe")
            passCierre = False
        else: 
            print("si existe")
            passCierre = True


        
        valorTotalIngresos = 0
        for ing_dia in ingresos_dia:
            valorTotalIngresos = ing_dia.valorIngreso + valorTotalIngresos
        
        valorTotalFacturas = 0
        for egresosEnFacturas in egre_facturas:
            valorTotalFacturas = valorTotalFacturas + egresosEnFacturas.valor

        valorTotalColaboradores = 0
        for egresosPagocolaboradores in egre_colaboradores:
            valorTotalColaboradores = valorTotalColaboradores + egresosPagocolaboradores.valor

        valorTotalPlanillasIees = 0
        for egresosPlanillasIees in egre_iess:
            valorTotalPlanillasIees = valorTotalPlanillasIees + egresosPlanillasIees.valor

        valorTotalDecinos = 0
        for egresosPagoDecimos in egre_decimos:
            valorTotalDecinos = valorTotalDecinos + egresosPagoDecimos.valor
    
        valorTotalServicios = 0
        for egrePagoServicios in egre_servicios:
            valorTotalServicios = valorTotalServicios + egrePagoServicios.valor

        valorTotalCreditos = 0
        for egresosPagoCreditos in egre_creditos:
            valorTotalCreditos = valorTotalCreditos + egresosPagoCreditos.valor
        
        valorTotalMovimientosIngreso = 0
        for TotalMovimientosIngreso in mov_movimientos_ingreso:
            valorTotalMovimientosIngreso = valorTotalMovimientosIngreso + TotalMovimientosIngreso.valor

        valorTotalMovimientosSalida = 0
        for TotalMovimientosSalida in mov_movimientos_salida:
            valorTotalMovimientosSalida = valorTotalMovimientosSalida + TotalMovimientosSalida.valor
        
        valorTotalEgresosSis = valorTotalFacturas + valorTotalColaboradores + valorTotalPlanillasIees + valorTotalDecinos + valorTotalServicios + valorTotalCreditos
        EmpresaMovimientosDia = empresa.objects.get(id=request.POST['empresa_selec']) 
        #valor_cierre_anterior = 0
        #for valor in cierreAnterior:
        #    valor_cierre_anterior = valor_cierre_anterior + valor.valorCierreActual

        return render(request, 'cierre_caja_empresa2.html',{
        #'form': form_cierres,
        'ingresos':ingresos_dia,
        'egrefac':egre_facturas,
        'egrecolaboradores':egre_colaboradores,
        'egre_iess':egre_iess,
        'egre_decimos':egre_decimos,
        'egre_servicios':egre_servicios,
        'egre_creditos':egre_creditos,
        'mov_movimientos_ingreso':mov_movimientos_ingreso,
        'mov_movimientos_salida':mov_movimientos_salida,

        'caja_id':caja_cierre.id,
        'empresa_id':request.POST['empresa_selec'],
        'fecha_consulta':fecha_filtro,  
        'passCierre':passCierre,
        
        'valorTotalEgresosSis':valorTotalEgresosSis,
        'valorTotalIngresos':valorTotalIngresos,
        'valorTotalFacturas' : valorTotalFacturas,
        'valorTotalColaboradores' : valorTotalColaboradores,
        'valorTotalPlanillasIees' : valorTotalPlanillasIees,
        'valorTotalDecinos':valorTotalDecinos,
        'valorTotalServicios':valorTotalServicios,
        'valorTotalCreditos':valorTotalCreditos,
        'valorTotalMovimientosIngreso':valorTotalMovimientosIngreso,
        'valorTotalMovimientosSalida': valorTotalMovimientosSalida,

        'EmpresaMovimientosDia':EmpresaMovimientosDia,

        })
    

#def cierresDiarios2(request):
#    if request.method == 'POST':
#        return render(request,'cierre_caja_empresa2.html')
#    else:
#        return render(request,'cierre_caja_empresa2.html')
    

def cierre3(request, caja_id, empresa_id,fecha_consulta):
    if request.method == 'GET':
        formato_str = "%Y-%m-%d"
        fecha_ayer = datetime.strptime(fecha_consulta,formato_str) - timedelta(days=1)
        ingresos_dia = ingresosCajas.objects.filter(nombreCaja=caja_id,empresaIngreso=empresa_id,fecha=fecha_consulta)
        egre_facturas = facturasProveedores.objects.filter(id_caja=caja_id,id_empresa=empresa_id,fechapago=fecha_consulta)
        egre_colaboradores = pagoColaboradores.objects.filter(id_caja=caja_id,id_empresa=empresa_id,fecha_pago=fecha_consulta)
        egre_iess = planillasIESS.objects.filter(caja=caja_id,id_empresa=empresa_id, fecha=fecha_consulta)
        egre_decimos = decimos.objects.filter(caja=caja_id,id_empresa=empresa_id, fecha=fecha_consulta)
        egre_servicios = pagoServicios.objects.filter(caja=caja_id,empresa_nuestra=empresa_id, fecha=fecha_consulta)
        egre_creditos = pagoCreditos.objects.filter(caja=caja_id,id_empresa=empresa_id, fecha=fecha_consulta)
        mov_movimientos_salida = movimientos.objects.filter(caja_origen_id=caja_id,empresaCaja=empresa_id, fecha=fecha_consulta)
        mov_movimientos_ingreso = movimientos.objects.filter(caja_destino_id=caja_id,empresaCaja=empresa_id, fecha=fecha_consulta)
        cierreAnterior = CierresCajas.objects.filter(caja=caja_id, empresa=empresa_id, fecha=fecha_ayer )
        
        valorTotalIngresos = 0
        for ing_dia in ingresos_dia:
            valorTotalIngresos = ing_dia.valorIngreso + valorTotalIngresos
        
        valorTotalFacturas = 0
        for egresosEnFacturas in egre_facturas:
            valorTotalFacturas = valorTotalFacturas + egresosEnFacturas.valor

        valorTotalColaboradores = 0
        for egresosPagocolaboradores in egre_colaboradores:
            valorTotalColaboradores = valorTotalColaboradores + egresosPagocolaboradores.valor

        valorTotalPlanillasIees = 0
        for egresosPlanillasIees in egre_iess:
            valorTotalPlanillasIees = valorTotalPlanillasIees + egresosPlanillasIees.valor

        valorTotalDecinos = 0
        for egresosPagoDecimos in egre_decimos:
            valorTotalDecinos = valorTotalDecinos + egresosPagoDecimos.valor
    
        valorTotalServicios = 0
        for egrePagoServicios in egre_servicios:
            valorTotalServicios = valorTotalServicios + egrePagoServicios.valor

        valorTotalCreditos = 0
        for egresosPagoCreditos in egre_creditos:
            valorTotalCreditos = valorTotalCreditos + egresosPagoCreditos.valor
        
        valorTotalMovimientosIngreso = 0
        for TotalMovimientosIngreso in mov_movimientos_ingreso:
            valorTotalMovimientosIngreso = valorTotalMovimientosIngreso + TotalMovimientosIngreso.valor

        valorTotalMovimientosSalida = 0
        for TotalMovimientosSalida in mov_movimientos_salida:
            valorTotalMovimientosSalida = valorTotalMovimientosSalida + TotalMovimientosSalida.valor

        valor_cierre_anterior = 0
        for valor in cierreAnterior:
            valor_cierre_anterior = valor_cierre_anterior + valor.valorCierreActual

        valorTotalEgresosSis = valorTotalFacturas + valorTotalColaboradores + valorTotalPlanillasIees + valorTotalDecinos + valorTotalServicios + valorTotalCreditos
        valorTotalDia = valorTotalIngresos - valorTotalEgresosSis + valorTotalMovimientosIngreso - valorTotalMovimientosSalida
        valor_cierre_dia = valorTotalDia + valor_cierre_anterior
        print('**************** caja')  
        print(ingresos_dia)
        print(len(ingresos_dia))
        return render(request, 'cierre_caja3.html',{
            'ingresos':ingresos_dia,
            'egrefac':egre_facturas,
            'egrecolaboradores':egre_colaboradores,
            'egre_iess':egre_iess,
            'egre_decimos':egre_decimos,
            'egre_servicios':egre_servicios,
            'egre_creditos':egre_creditos,
            'mov_movimientos_salida':mov_movimientos_salida,
            'mov_movimientos_ingreso' : mov_movimientos_ingreso,

            'valorTotalIngresos':valorTotalIngresos,
            'valorTotalFacturas' : valorTotalFacturas,
            'valorTotalColaboradores' : valorTotalColaboradores,
            'valorTotalPlanillasIees' : valorTotalPlanillasIees,
            'valorTotalDecinos':valorTotalDecinos,
            'valorTotalServicios':valorTotalServicios,
            'valorTotalCreditos':valorTotalCreditos,
            'valorTotalMovimientosIngreso':valorTotalMovimientosIngreso,
            'valorTotalMovimientosSalida': valorTotalMovimientosSalida,

            'valorTotalEgresosSis':valorTotalEgresosSis,
            'valorTotalDia':valorTotalDia,
            'valor_cierre_anterior':valor_cierre_anterior,
            'valor_cierre_dia':valor_cierre_dia ,

            'form':form_cierres,
        })
    else:


        formato_str = "%Y-%m-%d"
        fecha_ayer = datetime.strptime(fecha_consulta,formato_str) - timedelta(days=1)
        ingresos_dia = ingresosCajas.objects.filter(nombreCaja=caja_id,empresaIngreso=empresa_id,fecha=fecha_consulta)
        egre_facturas = facturasProveedores.objects.filter(id_caja=caja_id,id_empresa=empresa_id,fechapago=fecha_consulta)
        egre_colaboradores = pagoColaboradores.objects.filter(id_caja=caja_id,id_empresa=empresa_id,fecha_pago=fecha_consulta)
        egre_iess = planillasIESS.objects.filter(caja=caja_id,id_empresa=empresa_id, fecha=fecha_consulta)
        egre_decimos = decimos.objects.filter(caja=caja_id,id_empresa=empresa_id, fecha=fecha_consulta)
        egre_servicios = pagoServicios.objects.filter(caja=caja_id,empresa_nuestra=empresa_id, fecha=fecha_consulta)
        egre_creditos = pagoCreditos.objects.filter(caja=caja_id,id_empresa=empresa_id, fecha=fecha_consulta)
        mov_movimientos_salida = movimientos.objects.filter(caja_origen_id=caja_id,empresaCaja=empresa_id, fecha=fecha_consulta)
        mov_movimientos_ingreso = movimientos.objects.filter(caja_destino_id=caja_id,empresaCaja=empresa_id, fecha=fecha_consulta)
        cierreAnterior = CierresCajas.objects.filter(caja=caja_id, empresa=empresa_id, fecha=fecha_ayer )
        
        valorTotalIngresos = 0
        for ing_dia in ingresos_dia:
            valorTotalIngresos = ing_dia.valorIngreso + valorTotalIngresos
        
        valorTotalFacturas = 0
        for egresosEnFacturas in egre_facturas:
            valorTotalFacturas = valorTotalFacturas + egresosEnFacturas.valor

        valorTotalColaboradores = 0
        for egresosPagocolaboradores in egre_colaboradores:
            valorTotalColaboradores = valorTotalColaboradores + egresosPagocolaboradores.valor

        valorTotalPlanillasIees = 0
        for egresosPlanillasIees in egre_iess:
            valorTotalPlanillasIees = valorTotalPlanillasIees + egresosPlanillasIees.valor

        valorTotalDecinos = 0
        for egresosPagoDecimos in egre_decimos:
            valorTotalDecinos = valorTotalDecinos + egresosPagoDecimos.valor
    
        valorTotalServicios = 0
        for egrePagoServicios in egre_servicios:
            valorTotalServicios = valorTotalServicios + egrePagoServicios.valor

        valorTotalCreditos = 0
        for egresosPagoCreditos in egre_creditos:
            valorTotalCreditos = valorTotalCreditos + egresosPagoCreditos.valor
        
        valorTotalMovimientosIngreso = 0
        for TotalMovimientosIngreso in mov_movimientos_ingreso:
            valorTotalMovimientosIngreso = valorTotalMovimientosIngreso + TotalMovimientosIngreso.valor

        valorTotalMovimientosSalida = 0
        for TotalMovimientosSalida in mov_movimientos_salida:
            valorTotalMovimientosSalida = valorTotalMovimientosSalida + TotalMovimientosSalida.valor

        valor_cierre_anterior = 0
        for valor in cierreAnterior:
            valor_cierre_anterior = valor_cierre_anterior + valor.valorCierreActual

        valorTotalEgresosSis = valorTotalFacturas + valorTotalColaboradores + valorTotalPlanillasIees + valorTotalDecinos + valorTotalServicios + valorTotalCreditos
        valorTotalDia = valorTotalIngresos - valorTotalEgresosSis + valorTotalMovimientosIngreso - valorTotalMovimientosSalida
        valor_cierre_dia = valorTotalDia + valor_cierre_anterior
        
        empresaCierre = empresa.objects.get(id=empresa_id)
        cajaCierre = cajasReg.objects.get(id=caja_id)

        cierre_realizado = CierresCajas.objects.filter(empresa=empresaCierre, caja=cajaCierre, fecha=fecha_consulta)
    
        
        if not cierre_realizado.exists():
            nuevoRegDiario=CierresCajas(empresa=empresaCierre,caja=cajaCierre,fecha=fecha_consulta,valorIngresos=valorTotalIngresos,valorEgresos=valorTotalEgresosSis,valorMovSalida=valorTotalMovimientosSalida,valorMovEntrada=valorTotalMovimientosIngreso,valorCierreAnterior=valor_cierre_anterior,valorCierreActual=valor_cierre_dia,usuario=request.user)
            nuevoRegDiario.save()
            return redirect('cierresresumen')
        else: 
            return redirect('cierresresumen')



        
    

def CierresResumen(request):
    cajau = cajasReg.objects.filter(usuario=request.user)
    cajaid = cajau[0].id
    cierres2 = CierresCajas.objects.filter(caja=cajaid).order_by('-fecha')

    return render(request, 'resumenCierres.html',{
            'cierres':cierres2,
    })





def misMovimientos(request):
    if request.method == 'GET':
        fecha_consulta = datetime.now()
        cajau = cajasReg.objects.filter(usuario=request.user)
        cajaid = cajau[0].id

        ingresos_dia = ingresosCajas.objects.filter(nombreCaja=cajaid,fecha=fecha_consulta)
        egre_facturas = facturasProveedores.objects.filter(id_caja=cajaid,fechapago=fecha_consulta)
        egre_colaboradores = pagoColaboradores.objects.filter(id_caja=cajaid,fecha_pago=fecha_consulta)
        egre_iess = planillasIESS.objects.filter(caja=cajaid, fecha=fecha_consulta)
        egre_decimos = decimos.objects.filter(caja=cajaid, fecha=fecha_consulta)
        egre_servicios = pagoServicios.objects.filter(caja=cajaid, fecha=fecha_consulta)
        egre_creditos = pagoCreditos.objects.filter(caja=cajaid,fecha=fecha_consulta)
        mov_movimientos_salida = movimientos.objects.filter(caja_origen_id=cajaid,fecha=fecha_consulta)
        mov_movimientos_ingreso = movimientos.objects.filter(caja_destino_id=cajaid, fecha=fecha_consulta)
        cierreAnterior = CierresCajas.objects.filter(caja=cajaid, fecha=fecha_consulta )

        valorTotalIngresos = 0
        for ing_dia in ingresos_dia:
            valorTotalIngresos = ing_dia.valorIngreso + valorTotalIngresos
        
        valorTotalFacturas = 0
        for egresosEnFacturas in egre_facturas:
            valorTotalFacturas = valorTotalFacturas + egresosEnFacturas.valor

        valorTotalColaboradores = 0
        for egresosPagocolaboradores in egre_colaboradores:
            valorTotalColaboradores = valorTotalColaboradores + egresosPagocolaboradores.valor

        valorTotalPlanillasIees = 0
        for egresosPlanillasIees in egre_iess:
            valorTotalPlanillasIees = valorTotalPlanillasIees + egresosPlanillasIees.valor

        valorTotalDecinos = 0
        for egresosPagoDecimos in egre_decimos:
            valorTotalDecinos = valorTotalDecinos + egresosPagoDecimos.valor
    
        valorTotalServicios = 0
        for egrePagoServicios in egre_servicios:
            valorTotalServicios = valorTotalServicios + egrePagoServicios.valor

        valorTotalCreditos = 0
        for egresosPagoCreditos in egre_creditos:
            valorTotalCreditos = valorTotalCreditos + egresosPagoCreditos.valor
        
        valorTotalMovimientosIngreso = 0
        for TotalMovimientosIngreso in mov_movimientos_ingreso:
            valorTotalMovimientosIngreso = valorTotalMovimientosIngreso + TotalMovimientosIngreso.valor

        valorTotalMovimientosSalida = 0
        for TotalMovimientosSalida in mov_movimientos_salida:
            valorTotalMovimientosSalida = valorTotalMovimientosSalida + TotalMovimientosSalida.valor

        valor_cierre_anterior = 0
        for valor in cierreAnterior:
            valor_cierre_anterior = valor_cierre_anterior + valor.valorCierreActual

        valorTotalEgresosSis = valorTotalFacturas + valorTotalColaboradores + valorTotalPlanillasIees + valorTotalDecinos + valorTotalServicios + valorTotalCreditos

        return render(request, 'mis_movimientos.html',{
            'form': form_caja_empresa_cierre,
            'ingresos':ingresos_dia,
            'egrefac':egre_facturas,
            'egrecolaboradores':egre_colaboradores,
            'egre_iess':egre_iess,
            'egre_decimos':egre_decimos,
            'egre_servicios':egre_servicios,
            'egre_creditos':egre_creditos,
            'mov_movimientos_salida':mov_movimientos_salida,
            'mov_movimientos_ingreso':mov_movimientos_ingreso,

            'valorTotalIngresos':valorTotalIngresos,
            'valorTotalFacturas' : valorTotalFacturas,
            'valorTotalColaboradores' : valorTotalColaboradores,
            'valorTotalPlanillasIees' : valorTotalPlanillasIees,
            'valorTotalDecinos':valorTotalDecinos,
            'valorTotalServicios':valorTotalServicios,
            'valorTotalCreditos':valorTotalCreditos,
            'valorTotalMovimientosIngreso':valorTotalMovimientosIngreso,
            'valorTotalMovimientosSalida': valorTotalMovimientosSalida,

            'valorTotalEgresosSis':valorTotalEgresosSis,



        })
    else:
        caja_cierre = cajasReg.objects.get(usuario=request.user)
        fecha_filtro = request.POST['fecha']
        #ingresos_dia = ingresosCajas.objects.filter(nombreCaja=request.POST['caja_selec'],empresaIngreso=request.POST['empresa_selec']).order_by('-fecha')
        ingresos_dia = ingresosCajas.objects.filter(nombreCaja=caja_cierre ,empresaIngreso=request.POST['empresa_selec'],fecha=fecha_filtro)
        egre_facturas = facturasProveedores.objects.filter(id_caja=caja_cierre ,id_empresa=request.POST['empresa_selec'],fechapago=fecha_filtro)
        egre_colaboradores = pagoColaboradores.objects.filter(id_caja=caja_cierre ,id_empresa=request.POST['empresa_selec'],fecha_pago=fecha_filtro)
        egre_iess = planillasIESS.objects.filter(caja=caja_cierre ,id_empresa=request.POST['empresa_selec'], fecha=fecha_filtro)
        egre_decimos = decimos.objects.filter(caja=caja_cierre ,id_empresa=request.POST['empresa_selec'], fecha=fecha_filtro)
        egre_servicios = pagoServicios.objects.filter(caja=caja_cierre ,empresa_nuestra=request.POST['empresa_selec'], fecha=fecha_filtro)
        egre_creditos = pagoCreditos.objects.filter(caja=caja_cierre ,id_empresa=request.POST['empresa_selec'], fecha=fecha_filtro)
        mov_movimientos = movimientos.objects.filter(caja_origen_id=caja_cierre ,empresaCaja=request.POST['empresa_selec'], fecha=fecha_filtro)
        mov_movimientos_salida = movimientos.objects.filter(caja_origen_id=caja_cierre,empresaCaja=request.POST['empresa_selec'],fecha=fecha_filtro)
        mov_movimientos_ingreso = movimientos.objects.filter(caja_destino_id=caja_cierre,empresaCaja=request.POST['empresa_selec'], fecha=fecha_filtro)
        print("*******")
        print(mov_movimientos_ingreso)
        formato_str = "%Y-%m-%d"
       #fecha_ayer = datetime.strptime(fecha_consulta,formato_str) - timedelta(days=1)
        fecha_ayer = datetime.strptime(fecha_filtro,formato_str) - timedelta(days=1)
        empresaCierre = empresa.objects.get(id=request.POST['empresa_selec'])
        cajaCierre = cajasReg.objects.get(id=caja_cierre.id)

        cierre_realizado = CierresCajas.objects.filter(empresa=empresaCierre, caja=cajaCierre, fecha=fecha_ayer)
    
        passCierre = False
        if not cierre_realizado.exists():
            print("no existe")
            passCierre = False
        else: 
            print("si existe")
            passCierre = True


        
        valorTotalIngresos = 0
        for ing_dia in ingresos_dia:
            valorTotalIngresos = ing_dia.valorIngreso + valorTotalIngresos
        
        valorTotalFacturas = 0
        for egresosEnFacturas in egre_facturas:
            valorTotalFacturas = valorTotalFacturas + egresosEnFacturas.valor

        valorTotalColaboradores = 0
        for egresosPagocolaboradores in egre_colaboradores:
            valorTotalColaboradores = valorTotalColaboradores + egresosPagocolaboradores.valor

        valorTotalPlanillasIees = 0
        for egresosPlanillasIees in egre_iess:
            valorTotalPlanillasIees = valorTotalPlanillasIees + egresosPlanillasIees.valor

        valorTotalDecinos = 0
        for egresosPagoDecimos in egre_decimos:
            valorTotalDecinos = valorTotalDecinos + egresosPagoDecimos.valor
    
        valorTotalServicios = 0
        for egrePagoServicios in egre_servicios:
            valorTotalServicios = valorTotalServicios + egrePagoServicios.valor

        valorTotalCreditos = 0
        for egresosPagoCreditos in egre_creditos:
            valorTotalCreditos = valorTotalCreditos + egresosPagoCreditos.valor
        
        valorTotalMovimientosIngreso = 0
        for TotalMovimientosIngreso in mov_movimientos_ingreso:
            valorTotalMovimientosIngreso = valorTotalMovimientosIngreso + TotalMovimientosIngreso.valor

        valorTotalMovimientosSalida = 0
        for TotalMovimientosSalida in mov_movimientos_salida:
            valorTotalMovimientosSalida = valorTotalMovimientosSalida + TotalMovimientosSalida.valor
        
        valorTotalEgresosSis = valorTotalFacturas + valorTotalColaboradores + valorTotalPlanillasIees + valorTotalDecinos + valorTotalServicios + valorTotalCreditos
        EmpresaMovimientosDia = empresa.objects.get(id=request.POST['empresa_selec']) 
        #valor_cierre_anterior = 0
        #for valor in cierreAnterior:
        #    valor_cierre_anterior = valor_cierre_anterior + valor.valorCierreActual

        return render(request, 'mis_movimientos2.html',{
        #'form': form_cierres,
        'ingresos':ingresos_dia,
        'egrefac':egre_facturas,
        'egrecolaboradores':egre_colaboradores,
        'egre_iess':egre_iess,
        'egre_decimos':egre_decimos,
        'egre_servicios':egre_servicios,
        'egre_creditos':egre_creditos,
        'mov_movimientos_ingreso':mov_movimientos_ingreso,
        'mov_movimientos_salida':mov_movimientos_salida,

        'caja_id':caja_cierre.id,
        'empresa_id':request.POST['empresa_selec'],
        'fecha_consulta':fecha_filtro,  
        'passCierre':passCierre,
        
        'valorTotalEgresosSis':valorTotalEgresosSis,
        'valorTotalIngresos':valorTotalIngresos,
        'valorTotalFacturas' : valorTotalFacturas,
        'valorTotalColaboradores' : valorTotalColaboradores,
        'valorTotalPlanillasIees' : valorTotalPlanillasIees,
        'valorTotalDecinos':valorTotalDecinos,
        'valorTotalServicios':valorTotalServicios,
        'valorTotalCreditos':valorTotalCreditos,
        'valorTotalMovimientosIngreso':valorTotalMovimientosIngreso,
        'valorTotalMovimientosSalida': valorTotalMovimientosSalida,

        'EmpresaMovimientosDia':EmpresaMovimientosDia,

        })
    

def todosCierres(request):
    fecha_actual = datetime.now().date()
    fecha_inicial = fecha_actual - timedelta(days=30)
    cierrest = CierresCajas.objects.filter(fecha__range=[fecha_inicial,fecha_actual]).order_by('-fecha')
    gastoT = 0
    ingreT = 0
    for  cie in cierrest:
        gastoT = gastoT + cie.valorEgresos
        ingreT = ingreT + cie.valorIngresos


    return render(request,'todosCierres.html',{
        'cierrest':cierrest,
        'gastoT':gastoT,
        'ingreT':ingreT,

    })

def detallesCierres(request,cajaid,empresa_id,fecha_consulta):
    formato_str = "%Y-%m-%d"
    fecha_dia_anterior  = datetime.strptime(fecha_consulta,formato_str) - timedelta(days=1)
    ingresos_dia = ingresosCajas.objects.filter(nombreCaja=cajaid,fecha=fecha_consulta)
    egre_facturas = facturasProveedores.objects.filter(id_caja=cajaid,fechapago=fecha_consulta)
    egre_colaboradores = pagoColaboradores.objects.filter(id_caja=cajaid,fecha_pago=fecha_consulta)
    egre_iess = planillasIESS.objects.filter(caja=cajaid, fecha=fecha_consulta)
    egre_decimos = decimos.objects.filter(caja=cajaid, fecha=fecha_consulta)
    egre_servicios = pagoServicios.objects.filter(caja=cajaid, fecha=fecha_consulta)
    egre_creditos = pagoCreditos.objects.filter(caja=cajaid,fecha=fecha_consulta)
    mov_movimientos_salida = movimientos.objects.filter(caja_origen_id=cajaid,fecha=fecha_consulta)
    mov_movimientos_ingreso = movimientos.objects.filter(caja_destino_id=cajaid, fecha=fecha_consulta)
    cierreAnterior = CierresCajas.objects.filter(caja=cajaid, fecha=fecha_dia_anterior )

    valorTotalIngresos = 0
    for ing_dia in ingresos_dia:
        valorTotalIngresos = ing_dia.valorIngreso + valorTotalIngresos
        
    valorTotalFacturas = 0
    for egresosEnFacturas in egre_facturas:
        valorTotalFacturas = valorTotalFacturas + egresosEnFacturas.valor

    valorTotalColaboradores = 0
    for egresosPagocolaboradores in egre_colaboradores:
        valorTotalColaboradores = valorTotalColaboradores + egresosPagocolaboradores.valor

    valorTotalPlanillasIees = 0
    for egresosPlanillasIees in egre_iess:
        valorTotalPlanillasIees = valorTotalPlanillasIees + egresosPlanillasIees.valor

    valorTotalDecinos = 0
    for egresosPagoDecimos in egre_decimos:
        valorTotalDecinos = valorTotalDecinos + egresosPagoDecimos.valor
    
    valorTotalServicios = 0
    for egrePagoServicios in egre_servicios:
        valorTotalServicios = valorTotalServicios + egrePagoServicios.valor

    valorTotalCreditos = 0
    for egresosPagoCreditos in egre_creditos:
        valorTotalCreditos = valorTotalCreditos + egresosPagoCreditos.valor
        
    valorTotalMovimientosIngreso = 0
    for TotalMovimientosIngreso in mov_movimientos_ingreso:
        valorTotalMovimientosIngreso = valorTotalMovimientosIngreso + TotalMovimientosIngreso.valor

    valorTotalMovimientosSalida = 0
    for TotalMovimientosSalida in mov_movimientos_salida:
        valorTotalMovimientosSalida = valorTotalMovimientosSalida + TotalMovimientosSalida.valor

    valor_cierre_anterior = 0
    for valor in cierreAnterior:
        valor_cierre_anterior = valor_cierre_anterior + valor.valorCierreActual

    valorTotalEgresosSis = valorTotalFacturas + valorTotalColaboradores + valorTotalPlanillasIees + valorTotalDecinos + valorTotalServicios + valorTotalCreditos
    valorTotalDia = valorTotalIngresos - valorTotalEgresosSis + valorTotalMovimientosIngreso - valorTotalMovimientosSalida
    valor_cierre_dia = valorTotalDia + valor_cierre_anterior
    return render(request, 'detallesCierres.html',{
        'ingresos':ingresos_dia,
        'egrefac':egre_facturas,
        'egrecolaboradores':egre_colaboradores,
        'egre_iess':egre_iess,
        'egre_decimos':egre_decimos,
        'egre_servicios':egre_servicios,
        'egre_creditos':egre_creditos,
        'mov_movimientos_salida':mov_movimientos_salida,
        'mov_movimientos_ingreso':mov_movimientos_ingreso,

        'valorTotalIngresos':valorTotalIngresos,
        'valorTotalFacturas' : valorTotalFacturas,
        'valorTotalColaboradores' : valorTotalColaboradores,
        'valorTotalPlanillasIees' : valorTotalPlanillasIees,
        'valorTotalDecinos':valorTotalDecinos,
        'valorTotalServicios':valorTotalServicios,
        'valorTotalCreditos':valorTotalCreditos,
        'valorTotalMovimientosIngreso':valorTotalMovimientosIngreso,
        'valorTotalMovimientosSalida': valorTotalMovimientosSalida,

        'valorTotalEgresosSis':valorTotalEgresosSis,
        'valorTotalDia':valorTotalDia,
        'valor_cierre_anterior':valor_cierre_anterior,
        'valor_cierre_dia':valor_cierre_dia ,

    })