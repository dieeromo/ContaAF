# Generated by Django 3.0 on 2023-08-14 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_tipodecimo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0005_salidainstalaciones'),
    ]

    operations = [
        migrations.CreateModel(
            name='cierreInventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingreso_proveedores', models.DecimalField(decimal_places=2, max_digits=4)),
                ('ingreso_retiros', models.DecimalField(decimal_places=2, max_digits=4)),
                ('salida_instalaciones', models.DecimalField(decimal_places=2, max_digits=4)),
                ('salida_ventaContado', models.DecimalField(decimal_places=2, max_digits=4)),
                ('salida_ventaCredito', models.DecimalField(decimal_places=2, max_digits=4)),
                ('salida_dañados', models.DecimalField(decimal_places=2, max_digits=4)),
                ('fecha', models.DateField()),
                ('movimientos_entrada', models.DecimalField(decimal_places=2, max_digits=4)),
                ('movimientos_salida', models.DecimalField(decimal_places=2, max_digits=4)),
                ('total', models.DecimalField(decimal_places=2, max_digits=4)),
                ('observacion', models.CharField(blank=True, max_length=100, null=True)),
                ('digitador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('idBodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.bodega')),
                ('idEstatusUso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.nuevo_usado')),
                ('id_empresa', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='general.empresa')),
                ('idcodigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.codigo_prod')),
            ],
        ),
    ]