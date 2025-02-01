#from django.contrib import admin
#from . models import ingresosCajas
#from django.db.models import Sum


# Register your models here.
#class ingresosAdmin(admin.ModelAdmin):
#    list_display = ( 'fecha','nombreCaja', 'empresaIngreso','valorIngreso','conceptoIngreso','descripcion',)
#    list_filter = ('nombreCaja','empresaIngreso','conceptoIngreso')
#admin.site.register(ingresosCajas,ingresosAdmin)

from django.contrib import admin
from django.db.models import Sum
from .models import ingresosCajas

class IngresosCajasAdmin(admin.ModelAdmin):
    list_display = ('fecha',"nombreCaja", "empresaIngreso", "conceptoIngreso", "valorIngreso",)
    list_filter = ("nombreCaja", "empresaIngreso", "conceptoIngreso", "fecha")
    change_list_template = "admin/ingresos_cajas_change_list.html"

    def changelist_view(self, request, extra_context=None):
        # Obtener los filtros aplicados en la vista del admin
        queryset = self.get_queryset(request)

        # Calcular la suma de valorIngreso con los filtros aplicados
        total_ingresos = queryset.aggregate(total=Sum("valorIngreso"))["total"] or 0

        # Pasar el total a la plantilla del admin
        extra_context = extra_context or {}
        extra_context["total_ingresos"] = total_ingresos

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(ingresosCajas, IngresosCajasAdmin)

