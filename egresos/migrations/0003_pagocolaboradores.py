# Generated by Django 3.0 on 2023-05-22 02:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('egresos', '0002_auto_20230522_0219'),
    ]

    operations = [
        migrations.CreateModel(
            name='pagoColaboradores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('dias_normales', models.DecimalField(decimal_places=2, max_digits=4)),
                ('dias_extras', models.DecimalField(decimal_places=2, max_digits=4)),
                ('dias_feriados', models.DecimalField(decimal_places=2, max_digits=4)),
                ('fecha_pago', models.DateField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=6)),
                ('id_caja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.cajasReg')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.colaboradores')),
            ],
        ),
    ]
