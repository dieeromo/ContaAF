from django.contrib import admin
from .models import codigo_prod, nuevo_usado, bodega, ingresoFacturas, ingresosRetiros, clientes
from .models import  precioSalida, salidaInstalaciones, cierreInventario, salidaVentasContado
from .models import  movimimientosInventario, cierreInventario2
# Register your models here.


admin.site.register(codigo_prod)
admin.site.register(nuevo_usado)
admin.site.register(bodega)
admin.site.register(ingresoFacturas)
admin.site.register(ingresosRetiros)
admin.site.register(clientes)
admin.site.register(precioSalida)

class SalidasInstalacionesAdmin(admin.ModelAdmin):
    list_display = ('fecha_instalacion','idcodigo', 'cantidad','idEstatusUso','idcliente','idBodega')
    
admin.site.register(salidaInstalaciones,SalidasInstalacionesAdmin)



#admin.site.register(cierreInventario, CierreInventarioAdmin)

admin.site.register(salidaVentasContado)
admin.site.register(movimimientosInventario)
class CierreInventarioAdmin(admin.ModelAdmin):
    list_display = ('fecha','idBodega', 'idcodigo','idEstatusUso','cantidad','observacion')
    list_filter = ('fecha','idBodega')
admin.site.register(cierreInventario2,CierreInventarioAdmin)



