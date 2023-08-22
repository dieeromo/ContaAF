from django.db import models
from django.contrib.auth.models import User


class empresa(models.Model):
    nombreEmpresa = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombreEmpresa

class proveedoresProd(models.Model):
    nombreProveedor = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField(auto_now=True)
    seguimientoFacturas = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreProveedor
    

class tipoProducto(models.Model):
    nombreTipo = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nombreTipo

class modoCompra(models.Model):
    compra = models.CharField(max_length=100)
    def __str__(self):
        return self.compra
    
class estadoPago(models.Model):
    pago = models.CharField(max_length=100)
    def __str__(self):
        return self.pago
    
class marcasProducto(models.Model):
    nombreMarca = models.CharField(max_length=200)
    fechaCreacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombreMarca
    
class cajasReg(models.Model):
    nombreCaja = models.CharField(max_length=50)
    statusCaja = models.BooleanField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "{} ".format(self.nombreCaja)
    
class pagoMeses(models.Model):
    mes = models.CharField(max_length=50)
    def __str__(self):
        return self.mes

class pagoAnio(models.Model):
    anio = models.IntegerField()
    def __str__(self):
        return str(self.anio)

#class pagoAnio(models.Model):
#    anio = models.IntegerField()
#    def __int__(self):
#        return self.anio


class serviciosMensuales(models.Model):
    nombreServicio = models.CharField(max_length=200)
    def __str__(self):
        return "{}".format(self.nombreServicio)

class ingresosConcepto(models.Model):
    concepto = models.CharField(max_length=100)
    def __str__(self):
        return self.concepto
    
class colaboradores(models.Model):
    nombreColaborador = models.CharField(max_length=10)
    valorDia = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return self.nombreColaborador
    
class empresaServicio(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    def __str__(self):
        return "{}".format(self.nombre_empresa)

class institucionFinanciera(models.Model):
    nombre_finan = models.CharField(max_length=200)
    def __str__(self):
        return "{}".format(self.nombre_finan)
    

class tipoDecimo(models.Model):
    Tipo = models.CharField(max_length=200)
    def __str__(self):
        return "{}".format(self.Tipo)
    
