from typing import List
from fastapi import APIRouter, HTTPException
from models import PersonajeCreate, PersonajeResponse, PersonajeUpdate, RazaEnum
from database import leer_personajes, escribir_personajes

router = APIRouter(
    prefix="/personajes",
    tags=["CRUD Personajes (Modelo 3)"]
)

@router.get("", response_model=List[PersonajeResponse])
def listar_personajes(incluir_inactivos: bool = False):
    personajes = leer_personajes()
    if incluir_inactivos:
        return personajes
    return [p for p in personajes if p["activo"]]

@router.get("/buscar/{nombre}", response_model=PersonajeResponse)
def buscar_personaje_por_nombre(nombre: str):
    personajes = leer_personajes()
    personaje = next((p for p in personajes if p["nombre"].lower() == nombre.lower() and p["activo"]), None)
    if not personaje:
        raise HTTPException(status_code=404, detail=f"No se encontró un personaje activo llamado '{nombre}'")
    return personaje

@router.get("/filtrar/", response_model=List[PersonajeResponse])
def filtrar_personajes_por_raza(raza: RazaEnum):
    personajes = leer_personajes()
    return [p for p in personajes if p["raza"] == raza and p["activo"]]

@router.get("/{personaje_id}", response_model=PersonajeResponse)
def obtener_personaje_por_id(personaje_id: int):
    personajes = leer_personajes()
    personaje = next((p for p in personajes if p["id"] == personaje_id), None)
    if not personaje:
        raise HTTPException(status_code=404, detail=f"No se encontró el personaje con ID {personaje_id}")
    return personaje

@router.post("", response_model=PersonajeResponse, status_code=201)
def crear_personaje(personaje: PersonajeCreate):
    personajes = leer_personajes()
    nuevo_id = max([p["id"] for p in personajes], default=0) + 1
    nuevo_dict = {"id": nuevo_id, **personaje.model_dump()}
    personajes.append(nuevo_dict)
    escribir_personajes(personajes)
    return nuevo_dict

@router.put("/{personaje_id}", response_model=PersonajeResponse)
def actualizar_personaje(personaje_id: int, datos: PersonajeUpdate):
    personajes = leer_personajes()
    index = next((i for i, p in enumerate(personajes) if p["id"] == personaje_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail=f"No se encontró el personaje con ID {personaje_id}")
    
    personajes[index].update(datos.model_dump(exclude_unset=True))
    escribir_personajes(personajes)
    return personajes[index]

@router.delete("/{personaje_id}")
def eliminar_personaje_logico(personaje_id: int):
    personajes = leer_personajes()
    personaje = next((p for p in personajes if p["id"] == personaje_id), None)
    if not personaje:
        raise HTTPException(status_code=404, detail=f"No se encontró el personaje con ID {personaje_id}")
    
    personaje["activo"] = False
    escribir_personajes(personajes)
    return {"status": "success", "message": f"Personaje '{personaje['nombre']}' marcado como inactivo."}