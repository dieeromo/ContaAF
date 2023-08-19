from datetime import datetime, timedelta
from django.shortcuts import render
from general.models import pagoMeses
from cierres.models import CierresCajas
from egresos.models import pagoColaboradores, decimos, facturasProveedores, pagoServicios
from egresos.models import pagoCreditos, planillasIESS,Socios
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
        #cifrasdecimos_de = decimos.objects.filter(fecha__range=[fecha_inicial,fecha_actual])
        
        ingresostotalperiodo = 0
        egresostotalperiodo = 0
        for ingresos in cifrasCierres:
            ingresostotalperiodo = ingresostotalperiodo + ingresos.valorIngresos
            egresostotalperiodo = egresostotalperiodo + ingresos.valorEgresos
       
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

        gastos_total_eg = pagoCifrasIess +pagoCifrasCreditos+pagoCifrasServicios+pagoCifrasFacturas+pagoCifrasComi+pagoCifrasDeci+pagoColaboradoresTotal
        return render (request,'solidcifras.html',{
            'ingresostotalperiodo':ingresostotalperiodo,
            'egresostotalperiodo':egresostotalperiodo,
            'pagoColaboradoresTotal':pagoColaboradoresTotal,
            'pagoCifrasDeci':pagoCifrasDeci,
            'pagoCifrasComi':pagoCifrasComi,
            'pagoCifrasFacturas':pagoCifrasFacturas,
            'pagoCifrasServicios':pagoCifrasServicios,
            'pagoCifrasCreditos':pagoCifrasCreditos,
            'pagoCifrasIess':pagoCifrasIess,
            'gastos_total_eg':gastos_total_eg,

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
        
        cifrasdecimos_de = decimos.objects.filter(fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']],id_tipo=2)
        pagoCifrasDeci = 0
        for cifra_de in cifrasdecimos_de:
            pagoCifrasDeci = pagoCifrasDeci + cifra_de.valor
        
        cifrasdecimos_comi = decimos.objects.filter(fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']],id_tipo=1)
        pagoCifrasComi = 0
        for cifra_comi in cifrasdecimos_comi:
            pagoCifrasComi = pagoCifrasComi + cifra_comi.valor

        cifrasFacturas = facturasProveedores.objects.filter(fechapago__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagoCifrasFacturas = 0
        for cifFacturas in cifrasFacturas:
            pagoCifrasFacturas = pagoCifrasFacturas + cifFacturas.valor
        
        cifrasServicios = pagoServicios.objects.filter(fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagoCifrasServicios = 0
        for paser in cifrasServicios:
            pagoCifrasServicios = pagoCifrasServicios + paser.valor

        cifrascreditos = pagoCreditos.objects.filter(fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagoCifrasCreditos = 0
        for pacre in cifrascreditos:
            pagoCifrasCreditos = pagoCifrasCreditos + pacre.valor

        cifrasIess = planillasIESS.objects.filter(fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagoCifrasIess = 0
        for paIes in cifrasIess:
            pagoCifrasIess = paIes.valor + pagoCifrasIess

        egreSopcios = Socios.objects.filter(fecha__range=[request.POST['fecha_inicio'],request.POST['fecha_fin']])
        pagosocios_credi2 = 0
        for i in egreSopcios:
            pagosocios_credi2 = i.valor + pagosocios_credi2
        
        gastos_total_eg = pagoCifrasIess +pagoCifrasCreditos+pagoCifrasServicios+pagoCifrasFacturas+pagoCifrasComi+pagoCifrasDeci+pagoColaboradoresTotal+pagosocios_credi2

        return render (request, 'solidcifras.html',{
            'ingresostotalperiodo':ingresostotalperiodo,
            'egresostotalperiodo':egresostotalperiodo,

            'pagoColaboradoresTotal':pagoColaboradoresTotal,
            'pagoCifrasDeci':pagoCifrasDeci,
            'pagoCifrasComi':pagoCifrasComi,
            'pagoCifrasFacturas':pagoCifrasFacturas,
            'pagoCifrasServicios':pagoCifrasServicios,
            'pagoCifrasCreditos':pagoCifrasCreditos,
            'pagoCifrasIess':pagoCifrasIess,
            'gastos_total_eg':gastos_total_eg,
            'pagosocios_credi2':pagosocios_credi2,



            'fecha_inicio':request.POST['fecha_inicio'],
            'fecha_fin':request.POST['fecha_fin'],
        })

