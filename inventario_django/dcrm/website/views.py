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
    from .models import Profile, Record, Appointment

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        selected_role = request.POST.get('role')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Asegurar que el usuario tenga perfil
            profile, created = Profile.objects.get_or_create(
                user=user, 
                defaults={'role': 'Administrador' if user.is_superuser or user.is_staff else 'Cliente'}
            )
            
            if profile.role != selected_role:
                messages.error(request, f"🚫 Acceso denegado. No tienes el rol de {selected_role}.")
                return redirect('home')

            login(request, user)
            messages.success(request, f"Has iniciado sesión correctamente como {selected_role}")
            return redirect('home')
        else:
            messages.error(request, "Credenciales inválidas")
            return redirect('home')
    else:
        if request.user.is_authenticated:
            # Asegurar perfil
            profile, created = Profile.objects.get_or_create(
                user=request.user, 
                defaults={'role': 'Administrador' if request.user.is_superuser or request.user.is_staff else 'Cliente'}
            )
            
            if profile.role == 'Administrador':
                records = Record.objects.all()
                return render(request, 'home.html', {'records': records, 'role': 'Administrador'})
            else:
                # Cliente
                client_record = Record.objects.filter(user=request.user).first()
                appointments = []
                if client_record:
                    appointments = Appointment.objects.filter(record=client_record).order_by('fecha', 'hora')
                return render(request, 'home.html', {
                    'client_record': client_record,
                    'appointments': appointments,
                    'role': 'Cliente'
                })
        else:
            return render(request, 'home.html')

def login_user(request):
    return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('home')

def register_user(request):
    from .models import Profile, Record
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            
            # Crear perfil
            Profile.objects.create(user=user, role=role)
            
            # Si es cliente, registrar también en Record
            if role == 'Cliente':
                Record.objects.create(
                    user=user,
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name'),
                    email=form.cleaned_data.get('email'),
                    phone=form.cleaned_data.get('phone'),
                    address=form.cleaned_data.get('address'),
                    city=form.cleaned_data.get('city'),
                    state=form.cleaned_data.get('state'),
                    zipcode=form.cleaned_data.get('zipcode'),
                )
            
            messages.success(request, f"Usuario registrado correctamente como {role}")
            return redirect('home')
        else:
            messages.error(request, "Hubo un error en el registro. Por favor verifica los datos.")
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "🚫 No estás autenticado.")
        return redirect('home')
        
    from .models import Profile
    profile, created = Profile.objects.get_or_create(
        user=request.user, 
        defaults={'role': 'Administrador' if request.user.is_superuser or request.user.is_staff else 'Cliente'}
    )
    
    customer_record = Record.objects.get(id=pk)
    
    if profile.role == 'Administrador' or (profile.role == 'Cliente' and customer_record.user == request.user):
        return render(request, 'record.html', {'customer_record': customer_record, 'role': profile.role})
    else:
        messages.error(request, "🚫 No tienes permisos para ver este registro.")
        return redirect('home')

def delete_record(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "🚫 No estás autenticado.")
        return redirect('home')
        
    from .models import Profile
    profile, created = Profile.objects.get_or_create(
        user=request.user, 
        defaults={'role': 'Administrador' if request.user.is_superuser or request.user.is_staff else 'Cliente'}
    )
    
    if profile.role == 'Administrador':
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Registro eliminado exitosamente")
        return redirect('home')
    else:
        messages.error(request, "🚫 No tienes permisos para realizar esta acción.")
        return redirect('home')

def add_record(request):
    if not request.user.is_authenticated:
        messages.error(request, "🚫 No estás autenticado.")
        return redirect('home')
        
    from .models import Profile
    profile, created = Profile.objects.get_or_create(
        user=request.user, 
        defaults={'role': 'Administrador' if request.user.is_superuser or request.user.is_staff else 'Cliente'}
    )
    
    if profile.role == 'Administrador':
        form = AddRecordForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "📨 Registro agregado exitosamente")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "🚫 No tienes permisos para realizar esta acción.")
        return redirect('home')

def update_record(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "🚫 No estás autenticado.")
        return redirect('home')
        
    from .models import Profile
    profile, created = Profile.objects.get_or_create(
        user=request.user, 
        defaults={'role': 'Administrador' if request.user.is_superuser or request.user.is_staff else 'Cliente'}
    )
    
    current_record = Record.objects.get(id=pk)
    
    if profile.role == 'Administrador' or (profile.role == 'Cliente' and current_record.user == request.user):
        form = AddRecordForm(request.POST or None, instance=current_record)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Registro actualizado correctamente")
                return redirect('home')
        return render(request, 'update_record.html', {'form': form, 'role': profile.role})
    else:
        messages.error(request, "🚫 No tienes permisos para realizar esta acción.")
        return redirect('home')

def agenda(request):
    if not request.user.is_authenticated:
        messages.error(request, "🚫 Debes iniciar sesión")
        return redirect('home')

    from .models import Profile, Appointment
    profile, created = Profile.objects.get_or_create(
        user=request.user, 
        defaults={'role': 'Administrador' if request.user.is_superuser or request.user.is_staff else 'Cliente'}
    )

    if profile.role == 'Administrador':
        appointments = Appointment.objects.all().order_by('fecha', 'hora')
        form = AppointmentForm(request.POST or None)
    else:
        # Cliente
        client_record = Record.objects.filter(user=request.user).first()
        if client_record:
            appointments = Appointment.objects.filter(record=client_record).order_by('fecha', 'hora')
        else:
            appointments = []
        
        form = AppointmentForm(request.POST or None)
        # Filtrar queryset para que el cliente solo pueda seleccionarse a sí mismo
        if client_record:
            form.fields['record'].queryset = Record.objects.filter(id=client_record.id)
            form.fields['record'].initial = client_record
        else:
            form.fields['record'].queryset = Record.objects.none()

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Cita agendada correctamente")
            return redirect('agenda')

    return render(request, 'agenda.html', {'appointments': appointments, 'form': form, 'role': profile.role})

def delete_appointment(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
        
    from .models import Profile, Appointment
    profile, created = Profile.objects.get_or_create(
        user=request.user, 
        defaults={'role': 'Administrador' if request.user.is_superuser or request.user.is_staff else 'Cliente'}
    )
    
    appointment = Appointment.objects.get(id=pk)
    
    if profile.role == 'Administrador' or (profile.role == 'Cliente' and appointment.record.user == request.user):
        appointment.delete()
        messages.success(request, "Cita eliminada")
    else:
        messages.error(request, "🚫 No tienes permisos para realizar esta acción.")
        
    return redirect('agenda')

def update_appointment(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
        
    from .models import Profile, Appointment
    profile, created = Profile.objects.get_or_create(
        user=request.user, 
        defaults={'role': 'Administrador' if request.user.is_superuser or request.user.is_staff else 'Cliente'}
    )
    
    appointment = Appointment.objects.get(id=pk)
    
    if profile.role == 'Administrador' or (profile.role == 'Cliente' and appointment.record.user == request.user):
        form = AppointmentForm(request.POST or None, instance=appointment)
        
        if profile.role == 'Cliente':
            client_record = Record.objects.filter(user=request.user).first()
            if client_record:
                form.fields['record'].queryset = Record.objects.filter(id=client_record.id)
                
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "✅ Cita actualizada correctamente")
                return redirect('agenda')
                
        return render(request, 'update_appointment.html', {'form': form, 'role': profile.role})
    else:
        messages.error(request, "🚫 No tienes permisos para realizar esta acción.")
        return redirect('agenda')
        

    
        
    



