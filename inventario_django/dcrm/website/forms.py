#website/forms.py
# importacion de librerias y funciones para la creación de formularios en Django
from django import forms # para crear formularios en Django y sus campos.
from django.contrib.auth.forms import UserCreationForm # para crear un formulario de registro de usuarios basado en el modelo de usuario de Django.
from django.contrib.auth.models import User # para acceder al modelo de usuario de Django, que representa a los usuarios registrados en la base de datos.
##solicitudes dentro de la base de datos por que el formulario de registro de usuarios necesita verificar si el nombre de usuario ya existe en la base de datos.
# usando tecnologia  orm
#from .models import * # para importar todos los modelos definidos en el archivo models.py de la aplicación, lo que permite utilizarlos en la creación de formularios relacionados con esos modelos.
from .models import Record # para importar el modelo Record definido en el archivo models.py de la aplicación, lo que permite utilizarlo en la creación de formularios relacionados con ese modelo.#tipe ignore


# formulario de registro de usuarios personalizado que hereda de UserCreationForm
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'})) # campo de correo electrónico adicional para el formulario de registro de usuarios.


    # campos de primer nombre y apellido para el formulario de registro de usuarios.
    first_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nombre'})) # campo de primer nombre para el formulario de registro de usuarios.
    last_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Apellido'})) # campo de apellido para el formulario de registro de usuarios.
    class Meta:
        # atributos de la clase Meta para configurar el formulario de registro de usuarios.
        # La clase Meta se utiliza para configurar el formulario, especificando el modelo asociado y los campos que se incluirán en el formulario.
        model = User # especifica que el modelo asociado a este formulario es el modelo User de Django.
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2') # campos que se incluirán en el formulario de registro de usuarios, incluyendo el nombre de usuario, primer nombre, apellido, correo electrónico y las contraseñas.
        # los metodos
        
        def __init__(self,*args, **kwargs) -> None:
            # *args y **kwargs son parámetros que permiten pasar un número variable de argumentos posicionales y de palabras clave al método __init__. Esto es útil para permitir flexibilidad en la inicialización del formulario, ya que puede aceptar diferentes conjuntos de argumentos según sea necesario.inicializa el formulario utilizando el constructor de la clase padre UserCreationForm y luego personaliza los atributos de los campos del formulario
            super(SignUpForm, self).__init__(*args, **kwargs) # llama al constructor de la clase padre para inicializar el formulario.
            self.fields['username'].widget.attrs['class'] = 'form-control' # personaliza el campo de nombre de usuario agregando la clase CSS 'form-control' para mejorar su apariencia en el formulario.
            self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario' # personaliza el campo de nombre de usuario agregando un marcador de posición para indicar al usuario qué información se espera en ese campo.
            self.fields['username'].label= '' # personaliza el campo de nombre de usuario eliminando la etiqueta del campo para una apariencia más limpia en el formulario.
            self.fields['username'].help_text=('<span class="form-text text-muted"><small>Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.</small></span>') # personaliza el campo de nombre de usuario agregando un mensaje de ayuda para indicar al usuario los requisitos para el nombre de usuario.
            self.fields['password1'].widget.attrs['class'] = 'form-control' # personaliza el campo de contraseña 1 agregando la clase CSS 'form-control' para mejorar su apariencia en el formulario.
            self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña' # personaliza el campo de contraseña 1 agregando un marcador de posición para indicar al usuario qué información se espera en ese campo.
            self.fields['password1'].label= '' # personaliza el campo de contraseña 1 eliminando la etiqueta del campo para una apariencia más limpia en el formulario.
            self.fields['password1'].help_text=(
                
                '<ul class="form-text text-muted small">'
                '<li>Tu contraseña no puede ser demasiado similar a tu otra información personal.</li>'
                '<li>Tu contraseña debe contener al menos 8 caracteres.</li>'
                '<li>Tu contraseña no puede ser una contraseña común.</li>'
                '<li>Tu contraseña no puede ser completamente numérica.</li>'
                '</ul>'
            ) # personaliza el campo de contraseña 1 agregando un mensaje de ayuda para indicar al usuario los requisitos para la contraseña.
            #personaliza el campo de contraseña 2
            self.fields['password2'].widget.attrs['class'] = 'form-control' # personaliza el campo de contraseña 2 agregando la clase CSS 'form-control' para mejorar su apariencia en el formulario.
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña' # personaliza el campo de contraseña 2 agregando un marcador de posición para indicar al usuario qué información se espera en ese campo.
            self.fields['password2'].label= '' # personaliza el campo de contraseña 2 eliminando la etiqueta del campo para una apariencia más limpia en el formulario.
            self.fields['password2'].help_text=(
                '<span class="form-text text-muted"><small>'
                'Ingrese la misma contraseña que antes, para verificación.'
                '</small></span>'
            ) # personaliza el campo de contraseña 2 agregando un mensaje de ayuda para indicar al usuario los requisitos para la contraseña.
# ------------------ formulario agregar registro ------------------
# formulario par agregar registro del modelo Records    
class AddRecordForm(forms.ModelForm):
    # campo para el primer nombre , requerido , con placerholder y clase css
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"nombre","class":"forms-control"}), label="")
    #campos para el apellido , requerido, con placerholder y clase css
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Apellido","class":"forms-control"}), label="")
    #campo para el email , requerido, con placerholder y clase css  
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Correo electrónico","class":"forms-control"}), label="")
    #campo para el numero de telefono , requerido, con placerholder y clase css
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Número de teléfono","class":"forms-control"}), label="")
    #campo para la direccion , requerido, con placerholder y clase css
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Dirección","class":"forms-control"}), label="")
    #campo para el ciudad , requerido, con placerholder y clase css
    city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Ciudad","class":"forms-control"}), label="")
    #campo para el estado , requerido, con placerholder y clase css
    state = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Estado","class":"forms-control"}), label="")
    #campo para el codigo postal , requerido, con placerholder y clase css  
    zipcode = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Código postal","class":"forms-control"}), label="")
    #define el modelo  asociado y los cmapos requeridos
    class Meta:
        model = Record #el formulario se basa en el modelo Record
        exclude= ('user',) #excluye el campo 'user' del formulario, lo que significa que no se mostrará ni se podrá editar a través de este formulario. Esto es útil cuando el campo 'user' se establece automáticamente en función del usuario autenticado o se maneja de otra manera en la lógica de la aplicación.
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
