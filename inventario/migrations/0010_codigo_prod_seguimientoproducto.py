# Generated by Django 3.0 on 2023-08-22 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0009_cierreinventario2'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigo_prod',
            name='seguimientoProducto',
            field=models.BooleanField(default=True),
        ),
    ]