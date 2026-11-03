# Taller Angular CRUD + API REST + PostgreSQL

Este proyecto consiste en una aplicación CRUD completa con:
- Frontend en Angular
- Backend en FastAPI (Python)
- Base de datos PostgreSQL
- Arquitectura REST para gestión de empleados, departamentos, cargos y territorio (región, provincia, comuna)

## Stack tecnológico


- Angular 22
- FastAPI
- SQLAlchemy
- PostgreSQL 16
- Docker Compose
- Python 3.11+
- Node.js 20 LTS o superior

## Estructura del proyecto

```text
aller-angular-crud/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .venv/              # opcional, creada localmente
├── frontend/
│   ├── src/
│   ├── package.json
│   └── node_modules/      # opcional, creada localmente
├── docker-compose.yml
├── package-lock.json
└── README.md
```

## Requisitos previos

Instalá lo siguiente en tu máquina:

1. Docker Desktop o Docker Engine
2. Python 3.11 o superior
3. Node.js 20 LTS o superior
4. npm
5. Git

Verificá que estén disponibles con:

```powershell
python --version
node --version
npm --version
docker --version
```

## Credenciales y conexiones

### Base de datos PostgreSQL

La base se levanta con Docker Compose y usa esta configuración:

- Host: localhost
- Puerto: 5432
- Base de datos: empleados_db
- Usuario: postgres
- Password: postgres

URL de conexión de ejemplo:

```text
postgresql://postgres:postgres@localhost:5432/empleados_db
```

### Backend FastAPI

- URL base: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs

### Frontend Angular

- URL base: http://localhost:4200
- Ruta principal de empleados: http://localhost:4200/empleados

## Instalación

### 1) Clonar el proyecto

```powershell
git clone <url-del-repositorio>
cd C:\development\taller-angular-crud
```

### 2) Levantar la base de datos PostgreSQL

Desde la raíz del proyecto:

```powershell
cd C:\development\taller-angular-crud
docker compose up -d
```

Verificá que el contenedor esté corriendo:

```powershell
docker ps
```

Debe verse un contenedor con nombre similar a:
- taller-angular-crud-db

Validación de conexión:

```powershell
docker exec taller-angular-crud-db psql -U postgres -d empleados_db -c "SELECT current_database(), current_user, NOW();"
```

Debe devolver la base `empleados_db` junto con el usuario `postgres`.

## Levantar el backend

Abre una terminal en la carpeta `backend`:

```powershell
cd C:\development\taller-angular-crud\backend
```

Si no existe el entorno virtual, créalo:

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

Instalá dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Configura la variable de entorno de conexión a PostgreSQL:

```powershell
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/empleados_db"
```

Y levantá la API:

```powershell
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Si querés dejarlo corriendo en otra terminal sin perder la sesión, también podés abrir un nuevo PowerShell y repetir estos pasos.

### Verificar backend

Abrí esta URL:

```text
http://localhost:8000/docs
```

También podés consultar directamente los endpoints:

```powershell
Invoke-WebRequest http://localhost:8000/departamentos
Invoke-WebRequest http://localhost:8000/cargos
Invoke-WebRequest http://localhost:8000/regiones
```

## Levantar el frontend

Abre una terminal separada desde la carpeta `frontend`:

```powershell
cd C:\development\taller-angular-crud\frontend
npm install
npm start
```

Esto levanta Angular en:

```text
http://localhost:4200
```

Abrí la ruta:

```text
http://localhost:4200/empleados
```

## Cómo funciona la app

### Backend

El backend expone endpoints CRUD para:
- departamentos
- cargos
- empleados
- regiones
- provincias
- comunas

La API usa FastAPI y SQLAlchemy y conecta con PostgreSQL.

### Frontend

La app Angular consume la API y muestra:
- listados
- formularios de creación y edición
- validaciones
- alertas
- spinner de carga
- gestión de región, provincia y comuna según el flujo del empleado

## Datos semilla

Al iniciar la API, si la base está vacía, se insertan datos base como:
- regiones
- provincias
- comunas
- departamentos
- cargos
- un empleado de ejemplo

## Configuración del archivo .env

El backend tiene un ejemplo en `backend/.env.example`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/empleados_db
APP_ENV=development
```

Si querés usar un archivo `.env` real en `backend/`, podés crearlo con el mismo contenido. El proyecto también admite usar la variable de entorno `DATABASE_URL` desde PowerShell.

## Verificación final del flujo completo

Debe quedar así:

1. Docker funcionando en `localhost:5432`
2. Backend respondiendo en `http://localhost:8000`
3. Frontend levantado en `http://localhost:4200`
4. Ruta de empleados abierta: `http://localhost:4200/empleados`
5. Selectores cargados con departamentos, cargos y territorio

## Diagnóstico rápido

### Si la base no responde

```powershell
docker compose up -d
docker ps
docker logs taller-angular-crud-db
```

### Si el backend no responde

```powershell
cd C:\development\taller-angular-crud\backend
. .\.venv\Scripts\Activate.ps1
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/empleados_db"
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Si el frontend no carga datos

Verificá que el backend esté levantado en puerto 8000:

```powershell
Invoke-WebRequest http://localhost:8000/departamentos
```

Si esto responde con JSON, el frontend podrá consumirlo.

## Detener servicios

### Detener la base de datos

```powershell
cd C:\development\taller-angular-crud
docker compose down
```

### Detener backend y frontend

En cada terminal donde quedó corriendo el proceso:

```powershell
Stop-Process -Name python
Stop-Process -Name node
```

## Notas importantes

- La base de datos no se levanta con el frontend ni con el backend; debe correr por separado a través de Docker.
- El frontend no extrae datos directamente de PostgreSQL; hace llamadas a la API REST.
- El backend es la capa intermedia que conecta Angular con PostgreSQL.

## Datos de acceso resumidos

```text
DB host: localhost
DB port: 5432
Database: empleados_db
User: postgres
Password: postgres
API: http://localhost:8000
Frontend: http://localhost:4200
```

## Recomendación final

Para trabajar en local, conviene abrir 3 terminales separadas:

1. Terminal 1: Docker PostgreSQL
2. Terminal 2: Backend FastAPI
3. Terminal 3: Frontend Angular

Con esto tendrás el flujo completo funcionando correctamente.
