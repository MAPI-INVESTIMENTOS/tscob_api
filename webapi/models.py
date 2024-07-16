from django.db import models
from django.db import models
from datetime import datetime,timedelta,date
from django.contrib.auth.models import User
# Create your models here.
from simple_history.models import HistoricalRecords

import random
import string

def generate_alphanumeric_string():
    alphanumeric = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric) for _ in range(15))

class Empresa(models.Model):
    idEmpresa=models.BigAutoField(primary_key=True)
    nome=models.CharField(null=False, max_length=1000)
    nuit=models.CharField(null=False, max_length=1000)
    endereco=models.CharField(null=False, max_length=1000)
    vocacao=models.CharField(null=False, max_length=1000)
    objectivo=models.CharField(null=False, max_length=1000)
    Representante=models.CharField(null=False, max_length=1000)
    cidade=models.CharField(null=False, max_length=1000,default="Maputo")
    provinvia=models.CharField(null=False, max_length=1000,default="Maputo")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    history = HistoricalRecords()


class Pedidos_Quitacao(models.Model):
    idPedido = models.BigAutoField(primary_key=True)
    idEmpresa = models.ForeignKey(Empresa, null=True, on_delete=models.SET_NULL)
    estado=models.CharField(null=False, max_length=1000)
    estado_info = models.CharField(null=False, max_length=1000,default="processamento")
    estado_info_inter = models.CharField(null=False, max_length=1000, default="processamento")
    data_submisao=models.DateField(auto_now_add=True)
    tipo=models.CharField(null=False, max_length=1000, default="green")
    revisto=models.CharField(null=False, max_length=1000, default="0")
    assinalado=models.CharField(null=False, max_length=2, default="0")
    assinalado_er = models.CharField(null=False, max_length=2, default="0")
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    history = HistoricalRecords()


class Servicoes(models.Model):
    idServico = models.BigAutoField(primary_key=True)
    descricao=models.CharField(null=False, max_length=1000)
    valor=models.CharField(null=False, max_length=1000)

class Pagamnetos(models.Model):
    idPagamento=models.BigAutoField(primary_key=True)
    idEmpresa = models.ForeignKey(Empresa, null=True, on_delete=models.SET_NULL)
    valor=models.CharField(null=False, max_length=1000)
    descricao=models.CharField(null=False, max_length=1000)

class Quitacao(models.Model):
    idQuitacao=models.BigAutoField(primary_key=True)
    idPedido=models.ForeignKey(Pedidos_Quitacao, null=True, on_delete=models.SET_NULL)
    serialNumber=models.CharField(null=True, max_length=1000,unique=True)
    data_emissao=models.DateField(auto_now_add=True)
    data_expiracao=models.DateField()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.serialNumber:
            self.serialNumber = generate_alphanumeric_string()
        super(Quitacao, self).save(*args, **kwargs)

class Empresa_Quitacao(models.Model):
    idEmpresa=models.ForeignKey(Empresa, null=True, on_delete=models.SET_NULL)
    idQuitacao=models.ForeignKey(Quitacao, null=True, on_delete=models.SET_NULL)
    history = HistoricalRecords()

class Empresa_Atencedentes(models.Model):
    idAntecedente= models.BigAutoField(primary_key=True)
    idEmpresa = models.ForeignKey(Empresa, null=True, on_delete=models.SET_NULL)
    info=models.CharField(null=False, max_length=1000)
    data_submisao=models.DateField(auto_now_add=True)
