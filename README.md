# Formulario Backend

API REST construida con FastAPI y PostgreSQL para recibir y almacenar datos de un formulario, con subida de archivos a Google Drive.

## Stack

- **FastAPI** — framework de la API
- **SQLModel** — ORM (SQLAlchemy + Pydantic)
- **PostgreSQL** — base de datos
- **Pydantic Settings** — gestión de configuración vía `.env`

## Arquitectura por capas

```
app/
├── main.py        # Punto de entrada de la aplicación
├── core/          # Configuración, settings, .env, CORS
├── db/            # Conexión y sesión de la base de datos
├── models/        # Tablas de la base de datos (ORM)
├── schemas/       # Validación de entrada/salida (Pydantic)
├── services/      # Lógica de negocio (DB, Google Drive)
├── api/           # Endpoints / rutas
└── utils/         # Helpers: manejo de errores, logs
```

## Requisitos previos

- Python 3.10 o superior
- PostgreSQL corriendo en local

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd formulario-backend

# 2. Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate        # Linux / WSL2
# venv\Scripts\Activate.ps1      # Windows PowerShell

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Luego edita .env con tus credenciales reales
```

## Cómo correr el proyecto

```bash
fastapi dev app/main.py
```

La API quedará disponible en `http://localhost:8000`
Documentación interactiva (Swagger): `http://localhost:8000/docs`

## Variables de entorno

Ver `.env.example` para la lista completa de variables necesarias.
