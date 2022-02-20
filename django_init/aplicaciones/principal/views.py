from django.shortcuts import render
from .models import Criterio
from django.http import HttpResponse

# Create your views here.

def inicio(request):
    criterios=Criterio.objects.all()
    print(criterios)
    contexto={'criterios':criterios}
    return render(request,'index.html',contexto)
 # items=Criterio.objects.all()
 # for item in items:
 #     print(item.nombre)
 # return HttpResponse("La lista de criterios es la siguiente")