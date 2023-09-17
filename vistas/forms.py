from django import forms
from django.forms import ModelForm
from general.models import cajasReg, empresa
from cierres.models import CierresCajas

class form_seleccion_caja_empresa(forms.Form):
    choices_caja = [(opcion.id, opcion.nombreCaja) for opcion in cajasReg.objects.all()]
    choices_empresa = [(opcion2.id, opcion2.nombreEmpresa) for opcion2 in empresa.objects.all()]
    
    caja_selec = forms.ChoiceField(choices=choices_caja)
    empresa_selec = forms.ChoiceField(choices=choices_empresa)


class form_caja_empresa_cierre(forms.Form):
    #choices_caja = [(opcion.id, opcion.nombreCaja) for opcion in cajasReg.objects.all()]
    choices_empresa = [ (opcion2.id, opcion2.nombreEmpresa) for opcion2 in empresa.objects.all()]
    
    #caja_selec = forms.ChoiceField(choices=choices_caja)
    empresa_selec = forms.ChoiceField(choices=choices_empresa)
    #form_fecha = forms.DateField()

class form_cierres(ModelForm):
    class Meta:
        model = CierresCajas
        #fields = ['valorIngresos','valorEgresos','valorMovSalida', 'valorMovEntrada', 'valorCierreAnterior', 'valorCierreActual']
        fields = []

class form_Todoscierres(ModelForm):
    class Meta:
        model = CierresCajas
        fields = ['caja']
