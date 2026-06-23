from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AddRecordForm, SignUpForm
from .models import Record
from django.core.paginator import Paginator
from django.contrib.auth.models import User 
from .models import Record, Appointment
from .forms import SignUpForm, AppointmentForm




def home(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None: 
            login(request, user)

            messages.success(request, "has inicado sesion correctamente")
            return redirect('home')
        else:

            messages.error(request, "credenciales invalidas")

            return redirect('home')
    else:
        # Recupera todos los registros de la base de datos.
        records = Record.objects.all()
        # Renderiza la plantilla 'home.html' pasando los registros en el contexto.
        return render(request, 'home.html', {'records': records})

# Esta función define la vista de inicio de sesión (login) del sitio.


def login_user(request):
    return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('home')
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese usuario ya existe")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Usuario registrado correctamente")
        return redirect('home')
    
    return render(request, 'register.html')
        
   

def customer_record(request, pk):
    # Por ahora redirige a la página principal.
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.error(request, "🚫 no estas autentidicado entonces no se puede hacer esta accion")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Registro eliminado exitosamente")
        return redirect('home')
    else:
        messages.error(request, "🚫 no estas autentidicado entonces no se puede hacer esta accion")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record=form.save()
                messages.success(request," 📨 ya el registro fue agregado")
                return redirect('home')
        return render (request, 'add_record.html',{'form': form})
    else: # si el usuario no esta autentificado no le permite agregar registros
        messages.success(request," 🚫 no estas autentidicado entonces no se puede hacer esta accion")
        return redirect('home') # redirige a la pagina principal    

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form =AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro actualizado correctamente")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})

    else:
        messages.success(request, "🚫Error del usuario")
        return redirect('home')

def agenda(request):
    if not request.user.is_authenticated:
        messages.error(request, "🚫 Debes iniciar sesión")
        return redirect('home')

    appointments = Appointment.objects.all().order_by('fecha', 'hora')
    form = AppointmentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Cita agendada correctamente")
            return redirect('agenda')

    return render(request, 'agenda.html', {'appointments': appointments, 'form': form})

def delete_appointment(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
    appointment = Appointment.objects.get(id=pk)
    appointment.delete()
    messages.success(request, "Cita eliminada")
    return redirect('agenda')

def update_appointment(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
    
    appointment = Appointment.objects.get(id=pk)
    form = AppointmentForm(request.POST or None, instance=appointment)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Cita actualizada correctamente")
            return redirect('agenda')
    
    return render(request, 'update_appointment.html', {'form': form})
        

    
        
    



