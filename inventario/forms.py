from django.forms import ModelForm
from . models import ingresosRetiros, ingresoFacturas, salidaInstalaciones,cierreInventario2
from . models import salidaVentasContado, movimimientosInventario, clientes
from egresos.models import facturasProveedores

class form_registroInvRetiros(ModelForm):
    class Meta:
        model = ingresosRetiros
        fields = ['idcodigo','cantidad','idEstatusUso','idEstatusUso','idBodega','idcliente','observacion']

#class form_registroInvFacturas(ModelForm):
#    class Meta:
#        model = ingresoFacturas
#        fields = ['idcodigo','idEstatusUso','cantidad','precio_in','idFactura','idTipoProducto','idBodega','observacion']

class form_registroInvFacturas(ModelForm):
    class Meta:
        model = ingresoFacturas
        fields = ['idFactura','idcodigo','idEstatusUso','cantidad','precio_in','idTipoProducto','idBodega','observacion']
    
        labels = {
            'idFactura': '# Factura',
            'idcodigo': 'Códico Prod',
            'idEstatusUso': 'Uso', 
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        facturas_no_ingresadas = facturasProveedores.objects.exclude(estadoEntrega=True,)
        self.fields['idFactura'].queryset = facturas_no_ingresadas
        
class form_selecResumenInvFacturas(ModelForm):
    class Meta:
        model = ingresoFacturas
        fields = ['idFactura']
        labels = {
            'idFactura': '# Factura',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        facturas_ingresadas = facturasProveedores.objects.exclude(estadoEntrega=False)
        self.fields['idFactura'].queryset = facturas_ingresadas
    
class form_registroSalidasInstalaciones(ModelForm):
    class Meta:
        model = salidaInstalaciones
        fields = ['idcodigo','cantidad','idEstatusUso','precio','idcliente','idBodega','id_empresa','observacion']

class form_precierre(ModelForm):
    class Meta:
        model = cierreInventario2
        fields = ['idBodega','id_empresa']

class form_salidaVentasContado(ModelForm):
    class Meta:
        model = salidaVentasContado
        fields = ['idcodigo', 'cantidad','idEstatusUso','precio','idcliente','idBodega','id_empresa','id_estadoPago','observacion']

class form_movimientosInventario(ModelForm):
    class Meta:
        model = movimimientosInventario
        fields = ['id_empresa','idBodega_origen','idBodega_destino','idcodigo','idEstatusUso','cantidad','observacion']

class form_clientes_reg(ModelForm):
    class Meta:
        model = clientes
        fields = ['apenomb', 'nombre']
        labels = {
            'apenomb': 'Apellidos',
            'nombre':'Nombres'
        }
