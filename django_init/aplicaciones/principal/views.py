from django.shortcuts import render
from .models import Criterio, Website
from django.http import HttpResponse

# Create your views here.

def inicio(request):
    criterios=Criterio.objects.all()
    websites=Website.objects.all()
    contexto={'criterios':criterios,'websites':websites}
    if request.method=='GET':
        print("Invocacion via GET")   
     
        return render(request,'index.html',contexto)
    else:
          if request.method=='POST':
                 print(request)
                 print(request.__dict__)
                 print("Recuperando valor")
                 print(request.POST.get("Prueba1"))
                 print("invocaste a un post")
                 return render(request,'index.html',contexto)
 # items=Criterio.objects.all()
 # for item in items:
 #     print(item.nombre)
 # return HttpResponse("La lista de criterios es la siguiente")