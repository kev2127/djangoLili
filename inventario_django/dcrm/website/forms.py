#website/forms.py
# importacion de librerias y funciones para la creación de formularios en Django
from django import forms # para crear formularios en Django y sus campos.
from django.contrib.auth.forms import UserCreationForm # para crear un formulario de registro de usuarios basado en el modelo de usuario de Django.
from django.contrib.auth.models import User # para acceder al modelo de usuario de Django, que representa a los usuarios registrados en la base de datos.
##solicitudes dentro de la base de datos por que el formulario de registro de usuarios necesita verificar si el nombre de usuario ya existe en la base de datos.
# usando tecnologia  orm
#from .models import * # para importar todos los modelos definidos en el archivo models.py de la aplicación, lo que permite utilizarlos en la creación de formularios relacionados con esos modelos.
from .models import Record # para importar el modelo Record definido en el archivo models.py de la aplicación, lo que permite utilizarlo en la creación de formularios relacionados con ese modelo.#tipe ignore
from .models import Record, Appointment #Para el formulario de citas


# formulario de registro de usuarios personalizado que hereda de UserCreationForm
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'class': 'form-control'}))
    first_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}))
    last_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    # ← __init__ va AQUÍ, fuera de Meta
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Requerido. 150 caracteres o menos.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Mínimo 8 caracteres.</li>'
            '<li>No puede ser completamente numérica.</li>'
            '</ul>'
        )

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Ingresa la misma contraseña para verificación.</small></span>'
 # personaliza el campo de contraseña 2 agregando un mensaje de ayuda para indicar al usuario los requisitos para la contraseña.
# ------------------ formulario agregar registro ------------------
# formulario par agregar registro del modelo Records    

        from django import forms
from .models import Record

class AddRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'phone':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'address':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'city':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'state':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
            'zipcode':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código postal'}),
        }


class AppointmentForm(forms.ModelForm):
    record = forms.ModelChoiceField(
        queryset=Record.objects.all(),
        label='',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha = forms.DateField(
        label='',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    hora = forms.TimeField(
        label='',
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    descripcion = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'})
    )

    class Meta:
        model = Appointment
        fields = ('record', 'fecha', 'hora', 'descripcion')