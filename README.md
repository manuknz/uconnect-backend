# uConnect API

Proyecto de uConnect desarrollado con [FastAPI](https://fastapi.tiangolo.com/)

## EJECUTAR LOCALMENTE

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
- Crear o agregar archivo .env
- Buildear los contenedores:
```
docker-compose build
```
- Levantar los contenedores:
```
docker-compose up --detach --no-build db && docker-compose up --build server
```
- Para las siguientes veces solo basta con ejecutar:
```
docker-compose up
```
#### Para crear y aplicar migraciones del alembic
- Ingresamos al container para ejecutar el alembic:
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
- Construimos el container:
```
docker-compose up
```