from django.forms import ModelForm
from . models import ingresosRetiros, ingresoFacturas, salidaInstalaciones,cierreInventario
from . models import salidaVentasContado

class form_registroInvRetiros(ModelForm):
    class Meta:
        model = ingresosRetiros
        fields = ['idcodigo','cantidad','idEstatusUso','idEstatusUso','idBodega','idcliente','observacion']

class form_registroInvFacturas(ModelForm):
    class Meta:
        model = ingresoFacturas
        fields = ['idcodigo','idEstatusUso','cantidad','precio_in','idFactura','idTipoProducto','idBodega','observacion']

class form_registroSalidasInstalaciones(ModelForm):
    class Meta:
        model = salidaInstalaciones
        fields = ['idcodigo','cantidad','idEstatusUso','precio','idcliente','idBodega','id_empresa','observacion']

class form_precierre(ModelForm):
    class Meta:
        model = cierreInventario
        fields = ['idBodega']

class form_salidaVentasContado(ModelForm):
    class Meta:
        model = salidaVentasContado
        fields = ['idcodigo', 'cantidad','idEstatusUso','precio','idcliente','idBodega','id_empresa','id_estadoPago','observacion']