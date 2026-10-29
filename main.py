from fastapi import FastAPI
from database import inicializar_csv
from routers import sagas, transformaciones, personajes, combates

app = FastAPI(
    title="Dragon Ball Z Ki API - CRUD CSV Completo",
    description="API RESTful con CRUDs completos para 3 modelos (Sagas, Transformaciones, Personajes) con persistencia en CSV y borrado lógico",
    version="3.0.0"
)

# Inicializar almacenamiento CSV
inicializar_csv()

# Registrar los 3 modelos CRUD + Lógica de Combate
app.include_router(sagas.router)
app.include_router(transformaciones.router)
app.include_router(personajes.router)
app.include_router(combates.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "API de Dragon Ball Z activa con CRUDs en 3 modelos. Revisa /docs"}