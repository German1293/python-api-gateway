## Auth API

API de autenticación simple construida con **FastAPI**.

### Estructura del proyecto

- **app/main.py**: punto de entrada de la aplicación FastAPI.
- **app/core/**: configuración general, carga de variables de entorno y utilidades de seguridad (hash de contraseñas, JWT, etc.).
- **app/api/v1/**: routers de la versión 1 del API (`auth` y `health`).
- **app/models/**: modelos internos de dominio (ej. `User`).
- **app/schemas/**: esquemas Pydantic para peticiones y respuestas.
- **app/services/**: lógica de negocio (servicio de autenticación).
- **requirements.txt**: dependencias de Python.
- **Dockerfile**: imagen para ejecutar el servicio.
- **.env.example**: ejemplo de variables de entorno.

### Requisitos

- Python 3.11+
- pip

### Instalación local

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

### Variables de entorno

Copiar el archivo de ejemplo y ajustarlo:

```bash
cp .env.example .env
```

Editar `.env` y cambiar al menos:

- `SECRET_KEY`: clave secreta para firmar tokens JWT.
- `DEBUG`: `true` o `false`.

### Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

### Endpoints principales

- **GET** `/api/v1/health` – comprobación de estado.
- **POST** `/api/v1/auth/register` – registro de usuario.
- **POST** `/api/v1/auth/login` – login y obtención de token JWT.

### Ejecutar con Docker Compose + Nginx gateway

Este repositorio incluye un `docker-compose.yml` y un gateway Nginx que emula un Ingress:

- `auth-api`: contenedor con la API de autenticación (`uvicorn` en `auth-api:8000`).
- `iam-api`: contenedor con la API de IAM/usuarios (`iam-api:8000`).
- `auth-gateway`: contenedor Nginx que expone `8080:80` y enruta por path.
- `mongodb`: base de datos MongoDB.
- `redis`: caché Redis.
- `laboratory-network`: red bridge interna donde se conectan todos los servicios.

Rutas configuradas en el gateway:

- `/api/v1/auth/*` → `auth-api:8000` (público).
- `/api/v1/iam/*` → `iam-api:8000` protegido con `auth_request` (requiere header `Authorization`).
- `/api/v1/orders/*` → `auth-api:8000` protegido con `auth_request`.

El `auth_request` llama internamente a:

- `http://auth-api:8000/api/v1/auth/verify`

Para levantar todo (modo desarrollo):

```bash
cp .env.example .env  # si aún no lo hiciste
docker compose up -d --build
```

Para ver logs:

```bash
docker compose logs -f
```

Para apagar y limpiar contenedores del proyecto:

```bash
docker compose down
```

Luego puedes acceder a la API vía gateway en:

- `http://localhost:8080/api/v1/...`


