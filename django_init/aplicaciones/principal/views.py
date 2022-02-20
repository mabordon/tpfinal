from django.shortcuts import render
from .models import Criterio, Website
from django.http import HttpResponse

# Create your views here.

def inicio(request):
    if request.method=='GET':
        print("Invocacion via GET")
        criterios=Criterio.objects.all()
        websites=Website.objects.all()
        print(criterios)
        contexto={'criterios':criterios,'websites':websites}
        return render(request,'index.html',contexto)
    else:
          if request.method=='POST':
                 print(request)
                 print(request.__dict__)
                 print("Recuperando valor")
                 print(request.POST.get("Prueba1"))
                 print("invocaste a un post")
                 return render(request,'index.html')
 # items=Criterio.objects.all()
 # for item in items:
 #     print(item.nombre)
 # return HttpResponse("La lista de criterios es la siguiente")