from django.db import models
from general.models import empresa, cajasReg
from django.contrib.auth.models import User

# Create your models here.
class movimientos(models.Model):
    empresaCaja = models.ForeignKey(empresa, on_delete=models.CASCADE)
    caja_origen = models.ForeignKey(cajasReg, on_delete=models.CASCADE, related_name='movimientos_salida')
    caja_destino = models.ForeignKey(cajasReg, on_delete=models.CASCADE, related_name='movimientos_entrada')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=250)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.caja_origen, self.caja_destino, self.valor, self.fecha)