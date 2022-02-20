from django.db import models

# Create your models here.

# Create your models here.
class Criterio(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=200)

    def __str__(self):
         return self.nombre