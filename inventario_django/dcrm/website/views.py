from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AddRecordForm, SignUpForm
from .models import Record
from django.core.paginator import Paginator 



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
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have Registered!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form':form})
        
   

def customer_record(request, pk):
    # Por ahora redirige a la página principal.
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record':customer_record})
    else:
        messages.error(request, "🚫 no estas autentidicado entonces no se puede hacer esta accion")
        return redirect('home')

def delete_record(request, pk):
    # Por ahora redirige a la página principal.
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
        

    
        
    



