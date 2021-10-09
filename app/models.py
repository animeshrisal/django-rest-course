from django.db import models

# Create your models here.

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel')

class AnalyzedFile(models.Model):
    text = models.TextField()
    pos = models.FloatField()
    neg = models.FloatField()
    neu = models.FloatField()
    compound = models.FloatField()
    file = models.ForeignKey(ExcelFile, on_delete=models.CASCADE)
    