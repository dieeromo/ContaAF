from datetime import datetime, timedelta
from django.db.models import Sum, Q
from django.db.models.functions import ExtractMonth
from django.shortcuts import render
from general.models import pagoMeses, ingresosConcepto, empresa
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
        empresa_cifra = empresa.objects.get(nombreEmpresa="AFnet")
        fecha_inicio = '2023-05-31'
        
        fecha_actual = datetime.now().date()
        fecha_fin = fecha_actual - timedelta(days=3)
        
        cierre_inicial = CierresCajas.objects.filter(empresa=empresa_cifra,fecha=fecha_inicio)
        
        ingreso_inicial = 0
        egreso_inicial = 0
        cierre_anterior_inicial = 0
       
        for ii in cierre_inicial: 
            ingreso_inicial = ingreso_inicial + ii.valorIngresos
            egreso_inicial = egreso_inicial + ii.valorEgresos
            cierre_anterior_inicial = cierre_anterior_inicial + ii.valorCierreAnterior
            
        balance_inicial = ingreso_inicial - egreso_inicial + cierre_anterior_inicial

        cierrefinal = CierresCajas.objects.filter(empresa=empresa_cifra,fecha=fecha_fin)
        vtcierrefinal = 0
        for ii in cierrefinal:
            vtcierrefinal = vtcierrefinal + ii.valorCierreActual


        #se calcula el total de ingresos y egresos desde los cierres de caja
        cifrasCierres = CierresCajas.objects.filter(empresa=empresa_cifra,fecha__range=[fecha_inicio,fecha_fin])
        ingresostotalperiodo = 0
        egresostotalperiodo = 0
        for ingresos in cifrasCierres:
            ingresostotalperiodo = ingresostotalperiodo + ingresos.valorIngresos
            egresostotalperiodo = egresostotalperiodo + ingresos.valorEgresos

        #se calcula los ingresos desde los ingresos registrados
        ingresos_periodo = ingresosCajas.objects.filter(empresaIngreso=empresa_cifra,fecha__range=[fecha_inicio,fecha_fin])
        ingresosfiltradoperiodo = 0
        for ii in ingresos_periodo:
            ingresosfiltradoperiodo = ingresosfiltradoperiodo + ii.valorIngreso

        ingresos_detalle = []
        conceptosDeIngresos = ingresosConcepto.objects.all()
        for ii in conceptosDeIngresos:
            totalIngreConcepto = 0
            totalIngreConcepto = ingresosCajas.objects.filter( empresaIngreso = empresa_cifra,conceptoIngreso = ii.id, fecha__range=[fecha_inicio,fecha_fin]).aggregate(totalIngreConcepto =Sum('valorIngreso'))['totalIngreConcepto']
            data = {}
            data['concepto'] = ii.concepto
            data['valor']= totalIngreConcepto
            ingresos_detalle.append(data)
        
        print(ingresos_detalle)


    
        #se calcula el pago a los colaboradores desde el registro de pagos
        cifrasPagocolaboradores = pagoColaboradores.objects.filter(id_empresa=empresa_cifra,fecha_pago__range=[fecha_inicio,fecha_fin])
        pagoColaboradoresTotal= 0
        for col in cifrasPagocolaboradores:
            pagoColaboradoresTotal = pagoColaboradoresTotal + col.valor
        
        #se calcula el pago de decimos
        cifrasdecimos_de = decimos.objects.filter(id_empresa=empresa_cifra,fecha__range=[fecha_inicio,fecha_fin],id_tipo=2)
        pagoCifrasDeci = 0
        for cifra_de in cifrasdecimos_de:
            pagoCifrasDeci = pagoCifrasDeci + cifra_de.valor
            
        #se calcula el pago de comisiones
        cifrasdecimos_comi = decimos.objects.filter(id_empresa=empresa_cifra,fecha__range=[fecha_inicio,fecha_fin],id_tipo=1)
        pagoCifrasComi = 0
        for cifra_comi in cifrasdecimos_comi:
            pagoCifrasComi = pagoCifrasComi + cifra_comi.valor

        cifrasFacturas = facturasProveedores.objects.filter(id_empresa = empresa_cifra,fechapago__range=[fecha_inicio,fecha_fin])
        pagoCifrasFacturas = 0
        for cifFacturas in cifrasFacturas:
            pagoCifrasFacturas = pagoCifrasFacturas + cifFacturas.valor
        
        cifrasServicios = pagoServicios.objects.filter(empresa_nuestra=empresa_cifra,fecha__range=[fecha_inicio,fecha_fin])
        pagoCifrasServicios = 0
        for paser in cifrasServicios:
            pagoCifrasServicios = pagoCifrasServicios + paser.valor

        cifrascreditos = pagoCreditos.objects.filter(id_empresa=empresa_cifra,fecha__range=[fecha_inicio,fecha_fin])
        pagoCifrasCreditos = 0
        for pacre in cifrascreditos:
            pagoCifrasCreditos = pagoCifrasCreditos + pacre.valor

        cifrasIess = planillasIESS.objects.filter(id_empresa = empresa_cifra,fecha__range=[fecha_inicio,fecha_fin])
        pagoCifrasIess = 0
        for paIes in cifrasIess:
            pagoCifrasIess = paIes.valor + pagoCifrasIess
        
  
        egreSocios = Socios.objects.filter(id_empresa=empresa_cifra,fecha__range=[fecha_inicio,fecha_fin])
        pagosocios_credi2 = 0

        for i in egreSocios:
            pagosocios_credi2 = i.valor + pagosocios_credi2
        

        gastos_total_eg = pagoCifrasIess + pagoCifrasCreditos+pagoCifrasServicios+pagoCifrasFacturas+pagoCifrasComi+pagoCifrasDeci+pagoColaboradoresTotal+pagosocios_credi2


        totalfinalcierre = 0
        for  ii in cierrefinal:
            totalfinalcierre = totalfinalcierre + ii.valorCierreActual

        balance = ingresosfiltradoperiodo - gastos_total_eg
        return render (request, 'solidcifras.html',{
            'form' : form_selec_caja_cifras,
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

            'fecha_inicio':fecha_inicio,
            'fecha_fin': fecha_fin,
    

        })
    else:
        
        cierre_inicial = CierresCajas.objects.filter(empresa=request.POST['empresa'],fecha='2023-05-31')
        
        ingreso_inicial = 0
        egreso_inicial = 0
        cierre_anterior_inicial = 0
       
        for ii in cierre_inicial:
            ingreso_inicial = ingreso_inicial + ii.valorIngresos
            egreso_inicial = egreso_inicial + ii.valorEgresos
            cierre_anterior_inicial = cierre_anterior_inicial + ii.valorCierreAnterior
            
        balance_inicial = ingreso_inicial - egreso_inicial + cierre_anterior_inicial


        cierrefinal = CierresCajas.objects.filter(empresa=request.POST['empresa'],fecha=request.POST['fecha_fin'])
        vtcierrefinal = 0
        for ii in cierrefinal:
            vtcierrefinal = vtcierrefinal + ii.valorCierreActual


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
            data['valor']= totalIngreConcepto
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
        
        cifrasServicios = pagoServicios.objects.filter(empresa_nuestra=request.POST['empresa'],fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
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
        
  
        egreSocios = Socios.objects.filter(id_empresa=request.POST['empresa'],fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagosocios_credi2 = 0

        for i in egreSocios:
            pagosocios_credi2 = i.valor + pagosocios_credi2
        

        gastos_total_eg = pagoCifrasIess + pagoCifrasCreditos+pagoCifrasServicios+pagoCifrasFacturas+pagoCifrasComi+pagoCifrasDeci+pagoColaboradoresTotal+pagosocios_credi2


        totalfinalcierre = 0
        for  ii in cierrefinal:
            totalfinalcierre = totalfinalcierre + ii.valorCierreActual

        balance = ingresosfiltradoperiodo - gastos_total_eg
        return render (request, 'solidcifras.html',{
            'form' : form_selec_caja_cifras,
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

def historicos_mensuales(request):
    formato_str = "%Y-%m-%d"
    fecha_inicio_mano =  '2023-05-31'
    fecha_inicio = datetime.strptime(fecha_inicio_mano,formato_str)
    #mes_a_filtrar = 8

    meses_filtrar = [1,2,3,4,5,6,7,8,9,10,11,12]
    



    # Obtiene los registros del mes seleccionado
    for mes_a_filtrar in meses_filtrar:
        ingresoCajaMes = ingresosCajas.objects.filter(
            Q(empresaIngreso = 1 )&
            Q(fecha__month=mes_a_filtrar) &
            Q(fecha__year = datetime.now().year)
        ).aggregate(ingresoCajaMes=Sum('valorIngreso'))['ingresoCajaMes']  # Puedes ajustar el año si es necesario

        print(ingresoCajaMes)




    return render(request, 'historicosmensuales.html')
