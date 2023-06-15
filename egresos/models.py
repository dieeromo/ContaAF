from django.db import models
from django.contrib.auth.models import User
from general.models import proveedoresProd, modoCompra, estadoPago, empresa, cajasReg
from general.models import colaboradores, pagoMeses,pagoAnio, serviciosMensuales
from general.models import empresaServicio, institucionFinanciera, tipoDecimo
# Create your models here.


class facturasProveedores(models.Model):
    idproveedor = models.ForeignKey(proveedoresProd, on_delete=models.CASCADE)
    numeroFactura = models.CharField(max_length=100)
    fechafactura = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    id_modoCompra = models.ForeignKey(modoCompra, on_delete=models.CASCADE)
    id_estadoPago = models.ForeignKey(estadoPago, on_delete=models.CASCADE)
    fechapago = models.DateField(blank=True, null=True)
    estadoEntrega = models.BooleanField()
    fechaentrega = models.DateField(blank=True, null=True)
    id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_caja = models.ForeignKey(cajasReg, on_delete=models.CASCADE)
    observacion = models.CharField(max_length=200, blank=True)
    #creado = models.DateField(auto_now_add=True, default='2023-05-05')
    def __str__(self):
        return "{}  {}  // {}".format(self.idproveedor, self.fechapago,  self.valor)
    


class pagoColaboradores(models.Model):
   nombre = models.ForeignKey(colaboradores,on_delete=models.CASCADE)
   descripcion = models.CharField(max_length=200)
   dias_normales = models.DecimalField(max_digits=4, decimal_places=2)
   dias_extras = models.DecimalField(max_digits=4, decimal_places=2)
   dias_feriados = models.DecimalField(max_digits=4, decimal_places=2)
   fecha_pago = models.DateField()
   valor = models.DecimalField(max_digits=6, decimal_places=2)
   id_caja = models.ForeignKey(cajasReg, on_delete=models.CASCADE)
   id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
   id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, default=1)
   def __str__(self):
        return "{}  {}  {}".format(self.nombre,  self.fecha_pago,self.valor)
    


class  planillasIESS(models.Model):
    fecha = models.DateField()
    mesPago = models.ForeignKey(pagoMeses, on_delete=models.CASCADE)
    anio_pago = models.ForeignKey(pagoAnio, on_delete=models.CASCADE)
    colaborador = models.ForeignKey(colaboradores, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    caja = models.ForeignKey(cajasReg, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return "{}  {}  {}".format(self.colaborador, self.mesPago, self.valor)
    

class decimos(models.Model):
    colaborador = models.ForeignKey(colaboradores, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    caja = models.ForeignKey(cajasReg, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateField(auto_now_add=True)
    id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, default=1)
    id_tipo = models.ForeignKey(tipoDecimo, on_delete=models.CASCADE, default=2)
    def __str__(self):
        return "{}  {}  {}".format(self.colaborador, self.valor, self.id_tipo)
    
class pagoServicios(models.Model):

    servicio = models.ForeignKey(serviciosMensuales, on_delete=models.CASCADE)
    empresa_servicio =  models.ForeignKey(empresaServicio, on_delete=models.CASCADE)
    empresa_nuestra = models.ForeignKey(empresa, on_delete=models.CASCADE)
    mes_de_Pago = models.ForeignKey(pagoMeses, on_delete=models.CASCADE)
    anio_de_pago = models.ForeignKey(pagoAnio, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=200)
    caja = models.ForeignKey(cajasReg, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return "{} - {} - {} -  {}".format(self.empresa_nuestra, self.caja, self.servicio, self.valor)
    

class pagoCreditos(models.Model):

    nombre_coop = models.ForeignKey(institucionFinanciera, on_delete=models.CASCADE)
    mes_de_Pago = models.ForeignKey(pagoMeses, on_delete=models.CASCADE)
    anio_de_pago = models.ForeignKey(pagoAnio, on_delete=models.CASCADE)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    caja = models.ForeignKey(cajasReg, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado = models.DateField(auto_now_add=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return "{} - {} - {} -  {}".format(self.nombre_coop, self.valor, self.fecha, self.caja)
    
  
