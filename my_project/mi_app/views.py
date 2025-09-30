from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def formulario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        print(f"Nombre: {nombre}")
        print(f"Email: {email}")
        return HttpResponse("Datos recibidos. Revisa la consola del servidor.")
    
    return render(request, 'formulario.html')