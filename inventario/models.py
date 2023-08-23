from django.db import models
from django.contrib.auth.models import User
from egresos.models import facturasProveedores, estadoPago
from general.models import tipoProducto,empresa

# Create your models here.

class codigo_prod(models.Model):
    codigo = models.CharField(max_length=70)
    descripcion = models.CharField(max_length=250)
    fechaCreacion = models.DateTimeField(auto_now=True)
    seguimientoProducto = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.codigo)

class nuevo_usado(models.Model):
    estatus_uso = models.CharField(max_length=50)
    def __str__(self):
        return "{} ".format(self.estatus_uso)


class bodega(models.Model):
    nombre = models.CharField(max_length=60)
    fechaCreacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{} ".format(self.nombre)
    

class clientes(models.Model):
    apenomb = models.CharField(max_length=60)
    nombre = models.CharField(max_length=60, default='afnet')
    fechaCreacion = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{} {} ".format(self.apenomb, self.nombre)
    


class ingresoFacturas(models.Model):
    idcodigo = models.ForeignKey(codigo_prod, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)
    precio_in = models.DecimalField(max_digits=7, decimal_places=2)
    idFactura = models.ForeignKey(facturasProveedores, on_delete=models.CASCADE)
    idTipoProducto = models.ForeignKey(tipoProducto, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estadoIngreso = models.BooleanField() #false abierto - true cerrado
    idEstatusUso = models.ForeignKey(nuevo_usado, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(bodega, on_delete=models.CASCADE)
    precio_factura = models.DecimalField(max_digits=7, decimal_places=2)
    observacion = models.CharField(max_length=200, blank=True, null=True)


class ingresosRetiros(models.Model):
    idcodigo = models.ForeignKey(codigo_prod, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)
    idEstatusUso = models.ForeignKey(nuevo_usado, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(bodega, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField()
    idcliente = models.ForeignKey(clientes, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    observacion = models.CharField(max_length=200, blank=True,  null=True)
    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.cantidad, self.idcodigo, self.fecha_ingreso, self.idcliente, self.idBodega)

class precioSalida(models.Model):
    idcodigo = models.ForeignKey(codigo_prod, on_delete=models.CASCADE)
    idEstatusUso = models.ForeignKey(nuevo_usado, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    observacion = models.CharField(max_length=70, blank=True, null=True)
    def __str__(self):
        return "{}-{}-{} ".format(self.idcodigo, self.idEstatusUso, self.precio)

class salidaInstalaciones(models.Model):
    idcodigo = models.ForeignKey(codigo_prod, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=4, decimal_places=2)
    idEstatusUso = models.ForeignKey(nuevo_usado, on_delete=models.CASCADE)
    precio = models.ForeignKey(precioSalida,on_delete=models.CASCADE)
    idcliente = models.ForeignKey(clientes, on_delete=models.CASCADE)
    fecha_instalacion = models.DateField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    idBodega = models.ForeignKey(bodega, on_delete=models.CASCADE)
    id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, default=1)
    observacion = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return "{}-{}-{} ".format(self.idBodega, self.idcodigo, self.fecha_instalacion)


class salidaVentasContado(models.Model):
    idcodigo = models.ForeignKey(codigo_prod, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=4, decimal_places=2)
    idEstatusUso = models.ForeignKey(nuevo_usado, on_delete=models.CASCADE)
    precio = models.ForeignKey(precioSalida,on_delete=models.CASCADE)
    idcliente = models.ForeignKey(clientes, on_delete=models.CASCADE)
    fecha_venta = models.DateField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    observacion = models.CharField(max_length=100, blank=True, null=True)
    idBodega = models.ForeignKey(bodega, on_delete=models.CASCADE)
    id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, default=1)
    id_estadoPago = models.ForeignKey(estadoPago, on_delete=models.CASCADE)
    fecha_entrega = models.DateField(blank=True, null=True)
    def __str__(self):
        return "{}-{}-{} ".format(self.idBodega, self.idcodigo, self.fecha_venta)

    




class movimimientosInventario(models.Model):
    id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, default=1)
    idBodega_origen = models.ForeignKey(bodega, on_delete=models.CASCADE,related_name='movimientos_salida_inventario')
    idBodega_destino = models.ForeignKey(bodega, on_delete=models.CASCADE,related_name='movimientos_entrada_inventario')
    fecha = models.DateField()
    idcodigo = models.ForeignKey(codigo_prod, on_delete=models.CASCADE)
    idEstatusUso = models.ForeignKey(nuevo_usado, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=4, decimal_places=2)
    digitador = models.ForeignKey(User, on_delete=models.CASCADE)
    observacion = models.CharField(max_length=150, blank=True, null=True)
    creado = models.DateField(auto_now_add=True)
    def __str__(self):
        return "{}-{}-{}-{} ".format(self.idBodega_origen, self.idBodega_destino, self.fecha, self.idcodigo)

class cierreInventario(models.Model):
    idcodigo = models.ForeignKey(codigo_prod, on_delete=models.CASCADE)
    idEstatusUso = models.ForeignKey(nuevo_usado, on_delete=models.CASCADE)
    ingreso_proveedores = models.DecimalField(max_digits=4, decimal_places=2)
    ingreso_retiros = models.DecimalField(max_digits=4, decimal_places=2)
    salida_instalaciones = models.DecimalField(max_digits=4, decimal_places=2)
    salida_ventaContado = models.DecimalField(max_digits=4, decimal_places=2)
    salida_ventaCredito = models.DecimalField(max_digits=4, decimal_places=2)
    salida_dañados = models.DecimalField(max_digits=4, decimal_places=2)
    idBodega = models.ForeignKey(bodega, on_delete=models.CASCADE)
    id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, default=1)
    digitador = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    movimientos_entrada = models.DecimalField(max_digits=4, decimal_places=2)
    movimientos_salida = models.DecimalField(max_digits=4, decimal_places=2)
    total = models.DecimalField(max_digits=4, decimal_places=2)
    observacion = models.CharField(max_length=100, blank=True, null=True)

class cierreInventario2(models.Model):
    id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, default=1)
    idBodega = models.ForeignKey(bodega, on_delete=models.CASCADE)
    idcodigo = models.ForeignKey(codigo_prod, on_delete=models.CASCADE)
    idEstatusUso = models.ForeignKey(nuevo_usado, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=4, decimal_places=2)
    digitador = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    observacion = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return "{}-{}-{} ".format(self.idBodega, self.idcodigo, self.fecha)

    









    

