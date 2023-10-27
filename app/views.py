import datetime
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .forms import DuenoSignUpForm, ClienteSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Arrendamiento, Comuna, Estacionamiento, User, Cliente
import pytz
from datetime import datetime
from django.db.models import Q

def index(request):
    return render(request, 'accounts/index.html')

def register(request):
    return render(request, 'accounts/register.html')

class dueno_register(CreateView):
    model = User
    form_class = DuenoSignUpForm
    template_name = 'accounts/dueno_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class cliente_register(CreateView):
    model = User
    form_class = ClienteSignUpForm
    template_name = 'accounts/cliente_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Usuario o contraseña inválida")
        else:
            messages.error(request, "Usuario o contraseña inválida")
    return render(request, 'accounts/login.html', context={'form': AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

def lista_comunas(request):
    comunas = Comuna.objects.all()
    return render(request, 'app/buscar.html', {'comunas': comunas})

def buscar(request):
    comunas = Comuna.objects.all()  # Define comunas al principio de la función

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        hora_inicio = request.POST.get('hora_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        hora_fin = request.POST.get('hora_fin')
        comuna_seleccionada = request.POST.get('comuna_seleccionada')
        
        estacionamientos_disponibles = Estacionamiento.objects.all() 
        horas_totales = None 
        costo_por_hora = None 
        

        return render(request, 'estacionamiento/mostrar_estacionamiento.html', {
            'estacionamientos_disponibles': estacionamientos_disponibles,
            'horas_totales': horas_totales,
            'costo_por_hora': costo_por_hora,
            'comunas': comunas,
        })

    return render(request, 'estacionamiento/buscar.html', {'comunas': comunas})

# El resto de tu código (confirmar_reserva, pago_exitoso, arriendos, etc.) permanece igual.


def confirmar_reserva(request, estacionamiento_id):
    if request.user.is_authenticated:
        # User is logged in
        cliente = Cliente.objects.get(user=request.user)

        # Recuperar los datos almacenados en la sesión
        fecha_inicio = request.session.get('fecha_inicio')
        hora_inicio = request.session.get('hora_inicio')
        fecha_fin = request.session.get('fecha_fin')
        hora_fin = request.session.get('hora_fin')
        precio_total = request.session.get('precio_total')
        estacionamiento_id = request.session.get('estacionamiento')

        # Carga la instancia del Estacionamiento usando el ID
        estacionamiento = Estacionamiento.objects.get(pk=estacionamiento_id)

        tz = pytz.timezone('America/Santiago')

        fecha_inicio = tz.localize(datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S'))
        hora_inicio = tz.localize(datetime.strptime(hora_inicio, '%Y-%m-%d %H:%M:%S'))
        fecha_fin = tz.localize(datetime.strptime(fecha_fin, '%Y-%m-%d %H:%M:%S'))
        hora_fin = tz.localize(datetime.strptime(hora_fin, '%Y-%m-%d %H:%M:%S'))


        print("Datos recuperados de la sesión:")
        print("Cliente:", cliente)
        print("Fecha de inicio:", fecha_inicio)
        print("Hora de inicio:", hora_inicio)
        print("Fecha de fin:", fecha_fin)
        print("Hora de fin:", hora_fin)
        print("Precio total:", precio_total)
        print("ID del estacionamiento:", estacionamiento_id)

        # Crear un nuevo Arrendamiento y guardar los datos
        arrendamiento = Arrendamiento(
            cliente=cliente,
            estacionamiento=estacionamiento,
            fecha_inicio=fecha_inicio,
            hora_inicio=hora_inicio,
            fecha_fin=fecha_fin,
            hora_fin=hora_fin,
            precio=precio_total,
        )
        arrendamiento.save()

        # Redirige a la página de pago exitoso
        return redirect('pago_exitoso')

    else:
        # User is not logged in
        return redirect('login')
    
def pago_exitoso(request):
    # Lógica para la página de pago exitoso
    return render(request, 'estacionamiento/pago_exitoso.html')    



def arriendos(request):
    if request.user.is_authenticated:
        cliente = Cliente.objects.get(user=request.user)
        arrendamientos = Arrendamiento.objects.filter(cliente=cliente)
    else:
        arrendamientos = []

    return render(request, 'estacionamiento/arriendos.html', {'arrendamientos': arrendamientos})
