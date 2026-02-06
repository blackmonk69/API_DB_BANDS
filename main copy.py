from typing import Optional, List
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# Lee los valores
sqlite_url2 = os.getenv("sqlite_url")

if sqlite_url2 is None:
    raise RuntimeError("sqlite_url no está definida en el archivo .env")

class task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)
#sqlite_url = f"postgresql://neondb_owner:npg_eFCE9Qm7txMX@ep-lively-silence-aine4h5t-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# The engine is the central object to manage the database connection
# 
engine = create_engine(sqlite_url2, echo=True)



    
# Function to create the database and tables on application startup 
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica al arrancar (Startup)
    print("Iniciando aplicación y creando tablas...")
    SQLModel.metadata.create_all(engine, checkfirst=True)
    
    yield  # <--- Esto separa el arranque del apagado
    
    # Lógica al cerrar (Shutdown)
    print("Cerrando aplicación...")

# 2. Pasa la función SIN paréntesis al inicializar FastAPI
app = FastAPI(lifespan=lifespan)

# Dependency to get a database session for each request
#def get_session():
 #   with Session(engine) as session:
  #      yield session
 
# Path operation to create a new task
@app.post("/tasks/")
def create_task(task_param: task):
    with Session(engine) as session:
        session.add(task_param)
        session.commit()
        session.refresh(task_param) # Refresh to get the generated ID from the DB
        return task_param

# Path operation to read all tasks
@app.get("/tasks/")
def read_tasks():
    with Session(engine) as session:
           statement = select(task)
           tasks= session.exec(statement).all()
           return tasks
        
