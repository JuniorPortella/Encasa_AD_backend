from django.db import models

class Placas(models.Model):
    marca = models.CharField(max_length=250, null=True)
    modelo = models.CharField(max_length=250, null=True)
    watts = models.CharField(max_length=250, null=True)
    eficiencia = models.CharField(max_length=250, null=True)
    largura = models.CharField(max_length=250, null=True)
    altura = models.CharField(max_length=250, null=True)
    img = models.ImageField(upload_to='imagens/')


class SolarData(models.Model):
    LON = models.CharField(max_length=100, null=True)
    LAT = models.CharField(max_length=100, null=True)
    NAME = models.CharField(max_length=100, null=True)
    CLASS = models.CharField(max_length=100, null=True)
    STATE = models.CharField(max_length=100, null=True)
    ANNUAL = models.CharField(max_length=100, null=True)
    JAN = models.CharField(max_length=100, null=True)
    FEB = models.CharField(max_length=100, null=True)
    MAR = models.CharField(max_length=100, null=True)
    APR = models.CharField(max_length=100, null=True)
    MAY = models.CharField(max_length=100, null=True)
    JUN = models.CharField(max_length=100, null=True)
    JUL = models.CharField(max_length=100, null=True)
    AUG = models.CharField(max_length=100, null=True)
    SEP = models.CharField(max_length=100, null=True)
    OCT = models.CharField(max_length=100, null=True)
    NOV = models.CharField(max_length=100, null=True)
    DEC = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.NAME