# Generated by Django 3.0 on 2023-09-10 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0012_auto_20230822_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cierreinventario2',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='ingresofacturas',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='ingresosretiros',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
