from django.forms import ModelForm
from . models import movimientos


class form_movimientos(ModelForm):
    class Meta:
        model = movimientos
        fields = ['empresaCaja', 'caja_destino', 'valor', 'descripcion']