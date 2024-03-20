from django.db import models

# Create your models here.
class Utente(models.Model):
    nome=models.CharField()
    numero=