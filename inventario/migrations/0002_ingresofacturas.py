# Generated by Django 3.0 on 2023-08-10 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('egresos', '0011_socios'),
        ('general', '0004_tipodecimo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ingresoFacturas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=5)),
                ('precio_in', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fecha_ingreso', models.DateField()),
                ('estadoIngreso', models.BooleanField()),
                ('precio_factura', models.DecimalField(decimal_places=2, max_digits=5)),
                ('idBodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.bodega')),
                ('idEstatusUso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.nuevo_usado')),
                ('idFactura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='egresos.facturasProveedores')),
                ('idTipoProducto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.tipoProducto')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('idcodigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.codigo_prod')),
            ],
        ),
    ]
