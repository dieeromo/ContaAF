from django.db import models
from django.contrib.auth.models import User
from general.models import cajasReg, empresa, ingresosConcepto


# Create your models here.

class ingresosCajas(models.Model):
    nombreCaja = models.ForeignKey(cajasReg, on_delete=models.CASCADE)
    empresaIngreso = models.ForeignKey(empresa, on_delete=models.CASCADE)
    conceptoIngreso = models.ForeignKey(ingresosConcepto, on_delete=models.CASCADE)
    valorIngreso = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=300)
    creado = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - {} -  {}".format(self.nombreCaja, self.empresaIngreso, self.fecha, self.valorIngreso)
    

