# Generated by Django 3.0 on 2023-07-10 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0011_auto_20230710_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpedidos_quitacao',
            name='tipo',
            field=models.CharField(default='green', max_length=1000),
        ),
        migrations.AddField(
            model_name='pedidos_quitacao',
            name='tipo',
            field=models.CharField(default='green', max_length=1000),
        ),
    ]
