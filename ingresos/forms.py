from django import forms
from django.forms import ModelForm
from . models import ingresosCajas

#class form_registroIngresos(ModelForm):
#    class Meta:
#        model = ingresosCajas
#        fields = ['empresaIngreso', 'conceptoIngreso', 'valorIngreso', 'fecha', 'descripcion']

    
class form_registroIngresos(ModelForm):
    class Meta:
        model = ingresosCajas
        fields = ['empresaIngreso', 'conceptoIngreso', 'valorIngreso', 'descripcion']

    