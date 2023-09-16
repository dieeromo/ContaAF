from django.forms import ModelForm
from . models import facturasProveedores, pagoColaboradores, pagoServicios
from .models import pagoCreditos, decimos, planillasIESS

class form_registroFacturas(ModelForm):
    class Meta:
        model = facturasProveedores
        fields = ['idproveedor', 'numeroFactura','valor','id_modoCompra','id_estadoPago','id_empresa','observacion']
    
class form_todasfacturas(ModelForm):
    class Meta:
        model = facturasProveedores
        fields = ['id_empresa','id_caja']
class form_pagoColaboradores(ModelForm):
    class Meta:
        model = pagoColaboradores
        fields = ['nombre','descripcion','dias_normales','dias_extras','dias_feriados','valor','id_empresa']

class form_pre_pagoServicios(ModelForm):
    class Meta:
        model = pagoServicios
        fields = ['servicio','empresa_servicio','empresa_nuestra']
class form_pagoServicios(ModelForm):
    class Meta:
        model = pagoServicios
        fields = ['mes_de_Pago','anio_de_pago','valor','descripcion']

class form_PagoCreditos(ModelForm):
    class Meta:
        model = pagoCreditos
        fields = ['nombre_coop','mes_de_Pago','anio_de_pago','valor','descripcion','id_empresa']

class form_pagoDecimos(ModelForm):
    class Meta:
        model = decimos
        fields = ['id_empresa','colaborador','valor','id_tipo','descripcion',]

class form_planillasIess(ModelForm):
    class Meta:
        model = planillasIESS
        fields = ['colaborador','mesPago','anio_pago','descripcion','valor','id_empresa']

class form_pagarFacturas(ModelForm):
    class Meta:
        model = facturasProveedores
        fields = ['id_caja','id_estadoPago','observacion']

