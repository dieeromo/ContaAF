from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import render
from general.models import pagoMeses, ingresosConcepto
from cierres.models import CierresCajas
from egresos.models import pagoColaboradores, decimos, facturasProveedores, pagoServicios
from egresos.models import pagoCreditos, planillasIESS,Socios
from ingresos.models import ingresosCajas
from . forms import form_selec_caja_cifras

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
        
        
        ingreso_inicial = 0
        egreso_inicial = 0
        cierre_anterior_inicial = 0
        cierre_inicial = CierresCajas.objects.filter(fecha='2023-05-31')
        for ii in cierre_inicial:
            ingreso_inicial = ingreso_inicial + ii.valorIngresos 
            egreso_inicial = egreso_inicial + ii.valorEgresos
            cierre_anterior_inicial = cierre_anterior_inicial + ii.valorCierreAnterior
            
        balance_inicial = ingreso_inicial - egreso_inicial + cierre_anterior_inicial
       
        cierrefinal = CierresCajas.objects.filter(fecha=fecha_actual)
        vtcierrefinal = 0
        for ii in cierrefinal:
            vtcierrefinal = vtcierrefinal + ii.valorCierreActual
    
        #cifrasdecimos_de = decimos.objects.filter(fecha__range=[fecha_inicial,fecha_actual])    
        ingresostotalperiodo = 0
        egresostotalperiodo = 0

        for ingresos in cifrasCierres:
            ingresostotalperiodo = ingresostotalperiodo + ingresos.valorIngresos
            egresostotalperiodo = egresostotalperiodo + ingresos.valorEgresos
        
       
        ingresos_periodo = ingresosCajas.objects.filter(fecha__range=[fecha_inicial,fecha_actual])
        ingresosfiltradoperiodo = 0
        for ii in ingresos_periodo:
            ingresosfiltradoperiodo = ingresosfiltradoperiodo + ii.valorIngreso
    
    

        cifrasPagocolaboradores = pagoColaboradores.objects.filter(fecha_pago__range=[fecha_inicial,fecha_actual])
        pagoColaboradoresTotal= 0
        for col in cifrasPagocolaboradores:
            pagoColaboradoresTotal = pagoColaboradoresTotal + col.valor
        
        cifrasdecimos_de = decimos.objects.filter(fecha__range=[fecha_inicial,fecha_actual],id_tipo=1)
        pagoCifrasDeci = 0
        for cifra_de in cifrasdecimos_de:
            pagoCifrasDeci = pagoCifrasDeci + cifra_de.valor
        
        cifrasdecimos_comi = decimos.objects.filter(fecha__range=[fecha_inicial,fecha_actual],id_tipo=2)
        pagoCifrasComi = 0
        for cifra_comi in cifrasdecimos_comi:
            pagoCifrasComi = pagoCifrasComi + cifra_comi.valor

        cifrasFacturas = facturasProveedores.objects.filter(fechapago__range=[fecha_inicial,fecha_actual])
        pagoCifrasFacturas = 0
        for cifFacturas in cifrasFacturas:
            pagoCifrasFacturas = pagoCifrasFacturas + cifFacturas.valor

        cifrasServicios = pagoServicios.objects.filter(fecha__range=[fecha_inicial,fecha_actual])
        pagoCifrasServicios = 0
        for paser in cifrasServicios:
            pagoCifrasServicios = pagoCifrasServicios + paser.valor

        cifrascreditos = pagoCreditos.objects.filter(fecha__range=[fecha_inicial,fecha_actual])
        pagoCifrasCreditos = 0
        for pacre in cifrascreditos:
            pagoCifrasCreditos = pagoCifrasCreditos + pacre.valor

        cifrasIess = planillasIESS.objects.filter(fecha__range=[fecha_inicial,fecha_actual])
        pagoCifrasIess = 0
        for paIes in cifrasIess:
            pagoCifrasIess = paIes.valor + pagoCifrasIess
        
        egreSocios = Socios.objects.filter(fecha__range=[fecha_inicial,fecha_actual])
        pagosocios_credi2 = 0

        for ii in egreSocios:
            pagosocios_credi2 = ii.valor + pagosocios_credi2
        

        gastos_total_eg = pagoCifrasIess +pagoCifrasCreditos+pagoCifrasServicios+pagoCifrasFacturas+pagoCifrasComi+pagoCifrasDeci+pagoColaboradoresTotal+pagosocios_credi2
       
        totalfinalcierre = 0
        for  ii in cierrefinal:
            totalfinalcierre = totalfinalcierre + ii.valorCierreActual

        balance = ingresosfiltradoperiodo - gastos_total_eg
        return render (request,'solidcifras.html',{
            'form' : form_selec_caja_cifras,

        })
    else:
        
        cierre_inicial = CierresCajas.objects.filter(fecha='2023-05-31')
        
        ingreso_inicial = 0
        egreso_inicial = 0
        cierre_anterior_inicial = 0
       
        cierre_inicial = CierresCajas.objects.filter(fecha='2023-05-31')
        for ii in cierre_inicial:
            ingreso_inicial = ingreso_inicial + ii.valorIngresos
            egreso_inicial = egreso_inicial + ii.valorEgresos
            cierre_anterior_inicial = cierre_anterior_inicial + ii.valorCierreAnterior
            
        balance_inicial = ingreso_inicial - egreso_inicial + cierre_anterior_inicial


        cierrefinal = CierresCajas.objects.filter(fecha=request.POST['fecha_fin'])
        vtcierrefinal = 0
        for ii in cierrefinal:
            vtcierrefinal = vtcierrefinal + ii.valorCierreActual
        print("jhdbshjbdscjhbdshjbchjdsbchjdsbhjbsdchjbcdshjbdscjhbdscjhbdhjsbchjdsc%%%%%")
        print(request.POST['empresa'])

        #se calcula el total de ingresos y egresos desde los cierres de caja
        cifrasCierres = CierresCajas.objects.filter(empresa=request.POST['empresa'],fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        ingresostotalperiodo = 0
        egresostotalperiodo = 0
        for ingresos in cifrasCierres:
            ingresostotalperiodo = ingresostotalperiodo + ingresos.valorIngresos
            egresostotalperiodo = egresostotalperiodo + ingresos.valorEgresos

        #se calcula los ingresos desde los ingresos registrados
        ingresos_periodo = ingresosCajas.objects.filter(empresaIngreso=request.POST['empresa'],fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        ingresosfiltradoperiodo = 0
        for ii in ingresos_periodo:
            ingresosfiltradoperiodo = ingresosfiltradoperiodo + ii.valorIngreso

        ingresos_detalle = []
        conceptosDeIngresos = ingresosConcepto.objects.all()
        for ii in conceptosDeIngresos:
            totalIngreConcepto = 0
            totalIngreConcepto = ingresosCajas.objects.filter( empresaIngreso = request.POST['empresa'],conceptoIngreso = ii.id, fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']]).aggregate(totalIngreConcepto =Sum('valorIngreso'))['totalIngreConcepto']
            data = {}
            data['concepto'] = ii.concepto
            data['valor']= int(totalIngreConcepto or 0)
            ingresos_detalle.append(data)
        
        print(ingresos_detalle)


    
        #se calcula el pago a los colaboradores desde el registro de pagos
        cifrasPagocolaboradores = pagoColaboradores.objects.filter(id_empresa=request.POST['empresa'],fecha_pago__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagoColaboradoresTotal= 0
        for col in cifrasPagocolaboradores:
            pagoColaboradoresTotal = pagoColaboradoresTotal + col.valor
        
        #se calcula el pago de decimos
        cifrasdecimos_de = decimos.objects.filter(id_empresa=request.POST['empresa'],fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']],id_tipo=2)
        pagoCifrasDeci = 0
        for cifra_de in cifrasdecimos_de:
            pagoCifrasDeci = pagoCifrasDeci + cifra_de.valor
            
        #se calcula el pago de comisiones
        cifrasdecimos_comi = decimos.objects.filter(id_empresa=request.POST['empresa'],fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']],id_tipo=1)
        pagoCifrasComi = 0
        for cifra_comi in cifrasdecimos_comi:
            pagoCifrasComi = pagoCifrasComi + cifra_comi.valor

        cifrasFacturas = facturasProveedores.objects.filter(id_empresa = request.POST['empresa'],fechapago__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagoCifrasFacturas = 0
        for cifFacturas in cifrasFacturas:
            pagoCifrasFacturas = pagoCifrasFacturas + cifFacturas.valor
        
        cifrasServicios = pagoServicios.objects.filter(empresa_servicio=request.POST['empresa'],fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagoCifrasServicios = 0
        for paser in cifrasServicios:
            pagoCifrasServicios = pagoCifrasServicios + paser.valor

        cifrascreditos = pagoCreditos.objects.filter(id_empresa=request.POST['empresa'],fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagoCifrasCreditos = 0
        for pacre in cifrascreditos:
            pagoCifrasCreditos = pagoCifrasCreditos + pacre.valor

        cifrasIess = planillasIESS.objects.filter(id_empresa = request.POST['empresa'],fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagoCifrasIess = 0
        for paIes in cifrasIess:
            pagoCifrasIess = paIes.valor + pagoCifrasIess
        
  
        egreSocios = Socios.objects.filter(fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagosocios_credi2 = 0

        for i in egreSocios:
            pagosocios_credi2 = i.valor + pagosocios_credi2
        
        gastos_total_eg = pagoCifrasIess +pagoCifrasCreditos+pagoCifrasServicios+pagoCifrasFacturas+pagoCifrasComi+pagoCifrasDeci+pagoColaboradoresTotal+pagosocios_credi2


        totalfinalcierre = 0
        for  ii in cierrefinal:
            totalfinalcierre = totalfinalcierre + ii.valorCierreActual

        balance = ingresosfiltradoperiodo - gastos_total_eg
        return render (request, 'solidcifras.html',{
            'cierre_inicial' : cierre_inicial,
            'ingreso_inicial' : ingreso_inicial,
            'egreso_inicial' :  egreso_inicial,
            'cierre_anterior_inicial':cierre_anterior_inicial,
            'balance_inicial':balance_inicial,

            'vtcierrefinal':vtcierrefinal,
            'cierrefinal':cierrefinal,


            'ingresostotalperiodo':ingresostotalperiodo,
            'ingresos_detalle': ingresos_detalle,
            'egresostotalperiodo':egresostotalperiodo,
            'ingresosfiltradoperiodo':ingresosfiltradoperiodo,

            'pagoColaboradoresTotal':pagoColaboradoresTotal,
            'pagoCifrasDeci':pagoCifrasDeci,
            'pagoCifrasComi':pagoCifrasComi,
            'pagoCifrasFacturas':pagoCifrasFacturas,
            'pagoCifrasServicios':pagoCifrasServicios,
            'pagoCifrasCreditos':pagoCifrasCreditos,
            'pagoCifrasIess':pagoCifrasIess,
            'gastos_total_eg':gastos_total_eg,
            'pagosocios_credi2':pagosocios_credi2,
            
            'totalfinalcierre ':totalfinalcierre,
            'balance':balance,

            'fecha_inicio':request.POST['fecha_inicio'],
            'fecha_fin':request.POST['fecha_fin'],
        })

