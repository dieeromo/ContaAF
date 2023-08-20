from django.db import models
from general.models import empresa, cajasReg
from django.contrib.auth.models import User

# Create your models here.

class CierresCajas(models.Model):
    empresa = models.ForeignKey(empresa, on_delete=models.CASCADE)
    caja = models.ForeignKey(cajasReg, on_delete=models.CASCADE)
    fecha = models.DateField()
    valorIngresos = models.DecimalField(max_digits=10, decimal_places=2)
    valorEgresos = models.DecimalField(max_digits=10, decimal_places=2)
    valorMovSalida =  models.DecimalField(max_digits=10, decimal_places=2)
    valorMovEntrada = models.DecimalField(max_digits=10, decimal_places=2)
    valorCierreAnterior = models.DecimalField(max_digits=10, decimal_places=2)
    valorCierreActual = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "{}|{}|{}".format(self.caja, self.fecha, self.valorCierreActual)
    

