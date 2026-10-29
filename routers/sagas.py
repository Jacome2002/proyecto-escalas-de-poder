from typing import List
from fastapi import APIRouter, HTTPException
from models import SagaCreate, SagaResponse, SagaUpdate
from database import leer_sagas, escribir_sagas

router = APIRouter(
    prefix="/sagas",
    tags=["CRUD Sagas (Modelo 1)"]
)

@router.get("", response_model=List[SagaResponse])
def listar_sagas(incluir_inactivos: bool = False):
    sagas = leer_sagas()
    if incluir_inactivos:
        return sagas
    return [s for s in sagas if s["activo"]]

@router.get("/buscar/{nombre}", response_model=SagaResponse)
def buscar_saga_por_nombre(nombre: str):
    sagas = leer_sagas()
    saga = next((s for s in sagas if s["nombre"].lower() == nombre.lower() and s["activo"]), None)
    if not saga:
        raise HTTPException(status_code=404, detail=f"No se encontró la saga '{nombre}'")
    return saga

@router.get("/{saga_id}", response_model=SagaResponse)
def obtener_saga_por_id(saga_id: int):
    sagas = leer_sagas()
    saga = next((s for s in sagas if s["id"] == saga_id), None)
    if not saga:
        raise HTTPException(status_code=404, detail=f"No se encontró la saga con ID {saga_id}")
    return saga

@router.post("", response_model=SagaResponse, status_code=201)
def crear_saga(saga: SagaCreate):
    sagas = leer_sagas()
    nuevo_id = max([s["id"] for s in sagas], default=0) + 1
    nuevo_dict = {"id": nuevo_id, **saga.model_dump()}
    sagas.append(nuevo_dict)
    escribir_sagas(sagas)
    return nuevo_dict

@router.put("/{saga_id}", response_model=SagaResponse)
def actualizar_saga(saga_id: int, datos: SagaUpdate):
    sagas = leer_sagas()
    index = next((i for i, s in enumerate(sagas) if s["id"] == saga_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail=f"No se encontró la saga con ID {saga_id}")
    
    sagas[index].update(datos.model_dump(exclude_unset=True))
    escribir_sagas(sagas)
    return sagas[index]

@router.delete("/{saga_id}")
def eliminar_saga_logica(saga_id: int):
    sagas = leer_sagas()
    saga = next((s for s in sagas if s["id"] == saga_id), None)
    if not saga:
        raise HTTPException(status_code=404, detail=f"No se encontró la saga con ID {saga_id}")
    
    saga["activo"] = False
    escribir_sagas(sagas)
    return {"status": "success", "message": f"Saga '{saga['nombre']}' desactivada (borrado lógico en sagas.csv)."}