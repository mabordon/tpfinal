from django.db import models

# Create your models here.
class Criterio(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=200)

    