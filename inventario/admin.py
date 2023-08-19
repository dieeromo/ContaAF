from django.contrib import admin
from .models import codigo_prod, nuevo_usado, bodega, ingresoFacturas, ingresosRetiros, clientes
from .models import  precioSalida, salidaInstalaciones, cierreInventario, salidaVentasContado
# Register your models here.


admin.site.register(codigo_prod)
admin.site.register(nuevo_usado)
admin.site.register(bodega)
admin.site.register(ingresoFacturas)
admin.site.register(ingresosRetiros)
admin.site.register(clientes)
admin.site.register(precioSalida)
admin.site.register(salidaInstalaciones)
admin.site.register(cierreInventario)
admin.site.register(salidaVentasContado)



