# Psychoway CRM 🚀
### Sistema de Gestión de Registros y Control de Citas con Django y HTMX

**Psychoway CRM** es una aplicación web moderna diseñada para la administración ágil de clientes y citas. Integra un control de acceso basado en roles para diferenciar las actividades de los administradores y los clientes, ofreciendo una experiencia fluida de **Single Page Application (SPA)** mediante el uso de **HTMX** sin la complejidad de configurar frameworks de frontend pesados.

---

## 🌟 Características Principales

### 👥 Control de Acceso y Roles (RBAC)
* **Administradores:**
  * Control total de fichas de clientes (CRUD: Crear, Leer, Actualizar y Eliminar).
  * Panel global de agenda para visualizar, coordinar y gestionar todas las citas del sistema.
  * Asignación de profesionales responsables para cada cita.
* **Clientes:**
  * Autogestión de perfil y datos de contacto propios.
  * Visualización dedicada de su historial de citas agendadas.
  * Capacidad para agendar y cancelar citas propias de forma segura.

### ⚡ Navegación Fluida (Menú SPA)
* Navegación y envío de formularios dinámicos a través de **HTMX** (`hx-boost`).
* Carga asíncrona de páginas que elimina las recargas completas del navegador, optimizando el rendimiento y el consumo de ancho de banda.
* Gestión automática de historial y URL limpia en la barra de direcciones del navegador.

### 🛡️ Seguridad Implementada
* **Autenticación Segura:** Manejo de sesiones y contraseñas seguras a través del sistema de autenticación de Django.
* **Protección CSRF:** Protección contra ataques de falsificación de peticiones en sitios cruzados en todos los formularios.
* **Consultas Parametrizadas:** Uso del ORM de Django que previene de forma nativa ataques de inyección SQL.
* **Políticas de Cookies Estrictas:** Configuración para asegurar cookies de sesión y CSRF (HTTPS/HTTPOnly/SameSite) definidas en settings.
* **Validación de Formularios:** Validaciones en el cliente y backend para garantizar la integridad de los datos.

### 🎨 Interfaz de Usuario y UX
* Diseño adaptativo y limpio utilizando **Bootstrap 5** y tipografía **Inter**.
* Cierre automático de mensajes de alerta (`messages`) mediante temporizadores inteligentes.
* Modales de confirmación dinámicos y reutilizables para acciones destructivas o cambios críticos.

---

## 🛠️ Tecnologías y Librerías Utilizadas

* **Framework Principal:** [Django 5.0](https://www.djangoproject.com/)
* **Navegación Dinámica:** [HTMX 1.9.12](https://htmx.org/)
* **Estilos e Interfaz:** [Bootstrap 5](https://getbootstrap.com/)
* **Base de Datos:** MySQL / SQLite
* **Generación de Reportes / PDF:** `reportlab` y `weasyprint`
* **Manejo de Credenciales Seguras:** `python-dotenv`

---

## 📁 Estructura del Proyecto

El proyecto está organizado en la estructura clásica MVT de Django:

```text
djangoLili/
│
├── inventario_django/
│   ├── env/                      # Entorno virtual de Python
│   ├── requirements.txt          # Dependencias del proyecto
│   │
│   └── dcrm/                     # Directorio raíz de Django
│       ├── manage.py             # Script de administración de Django
│       │
│       ├── dcrm/                 # Configuración del proyecto
│       │   ├── settings.py       # Ajustes del sistema y seguridad
│       │   └── urls.py           # Enrutamiento de URLs global
│       │
│       └── website/              # Aplicación principal del CRM
│           ├── models.py         # Modelos (Profile, Record, Appointment)
│           ├── views.py          # Lógica de negocio y control de roles
│           ├── forms.py          # Formularios personalizados de Django
│           ├── urls.py           # Enrutamiento de URLs local
│           │
│           └── templates/        # Plantillas HTML
│               ├── base.html     # Estructura base, scripts globales e HTMX
│               ├── navbar.html   # Menú superior dinámico por roles
│               ├── home.html     # Dashboard de Admin y Cliente
│               ├── agenda.html   # Vista y formulario de citas
│               └── ...           # Formularios de adición, edición y registro
```

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para clonar y ejecutar el proyecto en tu entorno local:

### Prerrequisitos
* Python 3.10 o superior instalado.
* Servidor MySQL activo (si se configura la base de datos de producción).

### Paso 1: Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd djangoLili
```

### Paso 2: Configurar el Entorno Virtual
Crea un entorno virtual y actívalo para aislar las dependencias:

**En Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**En macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias
Instala los paquetes necesarios definidos en el archivo `requirements.txt`:
```bash
pip install -r inventario_django/requirements.txt
```

### Paso 4: Configurar Variables de Entorno
Crea un archivo `.env` en la raíz de la carpeta `dcrm/` (al mismo nivel que `manage.py`) para configurar los accesos de tu base de datos si utilizas MySQL:
```env
DB_NAME=tu_base_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contrasena
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Paso 5: Aplicar Migraciones
Prepara y ejecuta las migraciones para crear las tablas necesarias en la base de datos:
```bash
python inventario_django/dcrm/manage.py migrate
```

### Paso 6: Crear Superusuario (Administrador Inicial)
Crea una cuenta administrativa para tener acceso total al panel:
```bash
python inventario_django/dcrm/manage.py createsuperuser
```

### Paso 7: Iniciar el Servidor de Desarrollo
Inicia el servidor local de Django:
```bash
python inventario_django/dcrm/manage.py runserver
```
Abre tu navegador e ingresa a `http://127.0.0.1:8000/`.

---

## 🔒 Buenas Prácticas de Seguridad en el Proyecto

* **Variables Ocultas:** Las credenciales y claves secretas se cargan a través de `python-dotenv` y no se guardan directamente en el código fuente.
* **Control Fuerte de URL:** Si un usuario sin privilegios administrativos intenta acceder manualmente a rutas como `/add_record/` o `/delete_record/X`, la vista intercepta el rol en el perfil y redirige con un mensaje de alerta.
* **Separación Estricta de Datos:** El cliente solo tiene visibilidad e interacción sobre el registro asignado a su propio usuario mediante filtros a nivel de base de datos (`Record.objects.filter(user=request.user)`).

---

## 📄 Licencia
Este proyecto es de código abierto. Siéntete libre de clonarlo, adaptarlo y extender sus capacidades según tus necesidades.
