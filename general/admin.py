from django.contrib import admin
from . models import empresa, proveedoresProd, tipoProducto, modoCompra, estadoPago
from . models import marcasProducto, cajasReg, pagoMeses, pagoAnio
from . models import  serviciosMensuales, ingresosConcepto, colaboradores, empresaServicio
from . models import institucionFinanciera
# Register your models here.


admin.site.register(empresa)
admin.site.register(proveedoresProd)
admin.site.register(tipoProducto)
admin.site.register(modoCompra)
admin.site.register(estadoPago)
admin.site.register(marcasProducto)
admin.site.register(cajasReg)
admin.site.register(pagoMeses)
admin.site.register(pagoAnio)
admin.site.register(serviciosMensuales)
admin.site.register(ingresosConcepto)
admin.site.register(colaboradores)
admin.site.register(empresaServicio)
admin.site.register(institucionFinanciera)