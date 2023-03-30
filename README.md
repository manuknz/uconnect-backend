# uConnect API

Proyecto de uConnect desarrollado con [FastAPI](https://fastapi.tiangolo.com/)

## EJECUTAR LOCALMENTE

#### Primeros pasos

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
- Ingresamos al container para ejecutar el alembic:
```
docker-compose exec -it server bash                                            
```
- Creamos la migracion:
```
alembic revision -m "New Migration"
```
- Editamos el archivo generado manualmente con un editor de texto
- Aplicamos la migracion:
```
alembic upgrade head
```
