from django import forms
from django.forms import ModelForm
from cierres.models import CierresCajas


class form_selec_caja_cifras(ModelForm):
    class Meta:
        model = CierresCajas
        fields = ['empresa']