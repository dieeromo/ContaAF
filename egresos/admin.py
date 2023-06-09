from django.contrib import admin
from . models import facturasProveedores, pagoColaboradores, planillasIESS, decimos
from . models import pagoServicios, pagoCreditos
# Register your models here.
admin.site.register(facturasProveedores)
admin.site.register(pagoColaboradores)
admin.site.register(planillasIESS)
admin.site.register(decimos)
admin.site.register(pagoServicios)
admin.site.register(pagoCreditos)

