from django.contrib import admin
from . models import facturasProveedores, pagoColaboradores, planillasIESS, decimos
from . models import pagoServicios, pagoCreditos, Socios
# Register your models here.
#admin.site.register(facturasProveedores)
class PagoColaboradoresAdmin(admin.ModelAdmin):
    list_display = ( 'nombre','dias_normales', 'dias_extras','valor','fecha_ingreso','fecha_pago','estadoPagado','id_caja')
admin.site.register(pagoColaboradores,PagoColaboradoresAdmin)


admin.site.register(planillasIESS)

class PagoDecimosAdmin(admin.ModelAdmin):
    list_display = ( 'colaborador','id_tipo','descripcion','fecha','valor','caja')
admin.site.register(decimos, PagoDecimosAdmin)

admin.site.register(pagoServicios)  #son los pagos de servicios
admin.site.register(pagoCreditos)
admin.site.register(Socios)

class FacturasProveedoresAdmin(admin.ModelAdmin):
    list_display = ( 'fechafactura','idproveedor', 'numeroFactura','valor','id_caja','id_modoCompra','id_estadoPago','fechapago','estadoEntrega','fechaentrega','observacion')
    list_filter = ('id_empresa','id_caja','id_modoCompra','id_estadoPago')
admin.site.register(facturasProveedores,FacturasProveedoresAdmin)


