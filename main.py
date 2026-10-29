from fastapi import FastAPI
from database import inicializar_csv
from routers import sagas, transformaciones, personajes, combates

app = FastAPI(
    title="Dragon Ball Z Ki API - CRUD CSV Completo",
    description="API RESTful con CRUDs completos para 4 modelos (Sagas, Transformaciones, Personajes, Combates) con persistencia en CSV y borrado lógico",
    version="4.0.0"
)

# Inicializar archivos CSV
inicializar_csv()

# Registrar los 4 routers CRUD
app.include_router(sagas.router)
app.include_router(transformaciones.router)
app.include_router(personajes.router)
app.include_router(combates.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "API de Dragon Ball Z activa con CRUDs completos en 4 modelos. Revisa la documentación en /docs"}