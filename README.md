# uConnect API

Proyecto de uConnect desarrollado con [FastAPI](https://fastapi.tiangolo.com/)

## EJECUTAR LOCALMENTE

La maquina en la que querramos levantar el proyecto debe tener instalada estas dependencias:

- Python (version < 3.11) 
- Docker (con docker-compose)

### Primeros pasos para levantar el proyecto ya desarrollado

- Levantar el venv de Python:
```
python3 -m venv virtenv
```
- Activar el venv de Python:
```
source virtenv/bin/activate
```
- Instalar dependencias:
```
pip install -r requirements.txt
```
- Crear o agregar archivo .env con las credenciales para la base de datos en la raiz del proyecto.
- Crear o agregar archivo env.py con todas las variables de entorno del proyecto en app/env.
- Tambien pueden obtener estos archivos en este [GoogleDrive](https://drive.google.com/drive/folders/1FZFfCeO9K3Ri5VuVmICvBWA0v3HNBlgq?usp=drive_link), solicitando acceso.
- Buildear y levantar los contenedores:
```
docker-compose up --build
```
- Puede que tire un error porque el contenedor de la app se levanto antes que el de la BD. En ese caso podemos buildear y levantar ejecutando los siguientes comandos:
- Buildear los contenedores:
```
docker-compose build
```
- Levantar los contenedores:
```
docker-compose up --detach --no-build db && docker-compose up --build server nginx
```
- Para las siguientes veces que querramos correr solo basta con ejecutar:
```
docker-compose up
```
- Luego el swagger de la API estará disponible en `http://localhost/uconnect/api/docs#`
#### Para crear y aplicar migraciones del alembic
- Ingresamos al contenedor levantado para ejecutar el alembic:
```
docker-compose exec -it server bash       
```
- Creamos la migracion:
```
alembic revision -m "Nombre de la migracion"
```
- Editamos el archivo generado manualmente con un editor de texto
- Aplicamos la migracion:
```
alembic upgrade head
```
### Primeros pasos para empezar el proyecto

- Levantar el venv de Python:
```
python3 -m venv virtenv
```
- Activar el venv de Python:
```
source virtenv/bin/activate
```
- Instalar dependencias:
```
pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn python-dotenv
```
- Crear archivo .env
- Crear ruta y archivo app/env/env.py
- Crear archivo main.py
- Crear archivo Dockerfile
- Creamos archivo requirements.txt:
```
pip freeze > requirements.txt
```
- Crear archivo docker-compose.yml
- Crear archivo models.py
- Iniciar alembic:
```
alembic init alembic
```
- Construimos el contenedor:
```
docker-compose up
```