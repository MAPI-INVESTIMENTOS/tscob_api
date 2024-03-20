# Generated by Django 3.0 on 2023-08-29 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0016_auto_20230828_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa_Atencedentes',
            fields=[
                ('idAntecedente', models.BigAutoField(primary_key=True, serialize=False)),
                ('info', models.CharField(max_length=1000)),
                ('idEmpresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='webapi.Empresa')),
            ],
        ),
    ]
