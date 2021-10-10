from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AnalyzedFile(models.Model):
    text = models.TextField()
    pos = models.FloatField()
    neg = models.FloatField()
    neu = models.FloatField()
    compound = models.FloatField()
    file = models.ForeignKey(ExcelFile, on_delete=models.CASCADE)
    