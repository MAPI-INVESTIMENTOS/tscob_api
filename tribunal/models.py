from django.db import models

# Create your models here.
class Tribunal_(models.Model):
    nome=models.CharField()
    provincia=models.CharField()
    enderco=models.CharField()
    contato=models.CharField()
    email=models.CharField()

class Distribuidor(models.Model):
    nome=models.CharField()
    nrBi=models.CharField()
    contato=models.CharField()
    email=models.CharField()

class Arquivo(models.Model):
    nome=models.CharField()
