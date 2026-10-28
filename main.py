from fastapi import FastAPI
from database import inicializar_csv
from routers import personajes, combates

app = FastAPI(
    title="Dragon Ball Z Ki API - CRUD CSV",
    description="API RESTful modularizada con APIRouter para niveles de Ki y combates en DBZ",
    version="2.0.0"
)

# Inicializar almacenamiento al arrancar
inicializar_csv()

# Registrar los módulos de rutas
app.include_router(personajes.router)
app.include_router(combates.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido a la API de Dragon Ball Z. Revisa la documentación en /docs"}