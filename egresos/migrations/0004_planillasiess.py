# Generated by Django 3.0 on 2023-05-22 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
        ('egresos', '0003_pagocolaboradores'),
    ]

    operations = [
        migrations.CreateModel(
            name='planillasIESS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('descripcion', models.CharField(max_length=200)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('anio_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.pagoAnio')),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.cajasReg')),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.colaboradores')),
                ('mesPago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.pagoMeses')),
            ],
        ),
    ]