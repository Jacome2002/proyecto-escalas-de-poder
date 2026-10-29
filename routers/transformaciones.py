from typing import List
from fastapi import APIRouter, HTTPException
from models import TransformacionCreate, TransformacionResponse, TransformacionUpdate
from database import leer_transformaciones, escribir_transformaciones

router = APIRouter(
    prefix="/transformaciones",
    tags=["CRUD Transformaciones (Modelo 2)"]
)

@router.get("", response_model=List[TransformacionResponse])
def listar_transformaciones(incluir_inactivos: bool = False):
    trans = leer_transformaciones()
    if incluir_inactivos:
        return trans
    return [t for t in trans if t["activo"]]

@router.get("/buscar/{nombre}", response_model=TransformacionResponse)
def buscar_transformacion_por_nombre(nombre: str):
    trans = leer_transformaciones()
    t = next((tr for tr in trans if tr["nombre"].lower() == nombre.lower() and tr["activo"]), None)
    if not t:
        raise HTTPException(status_code=404, detail=f"No se encontró la transformación '{nombre}'")
    return t

@router.get("/filtrar/", response_model=List[TransformacionResponse])
def filtrar_por_multiplicador_minimo(min_multiplicador: float):
    trans = leer_transformaciones()
    return [t for t in trans if t["multiplicador_ki"] >= min_multiplicador and t["activo"]]

@router.get("/{trans_id}", response_model=TransformacionResponse)
def obtener_transformacion_por_id(trans_id: int):
    trans = leer_transformaciones()
    t = next((tr for tr in trans if tr["id"] == trans_id), None)
    if not t:
        raise HTTPException(status_code=404, detail=f"No se encontró la transformación con ID {trans_id}")
    return t

@router.post("", response_model=TransformacionResponse, status_code=201)
def crear_transformacion(trans: TransformacionCreate):
    t_list = leer_transformaciones()
    nuevo_id = max([tr["id"] for tr in t_list], default=0) + 1
    nuevo_dict = {"id": nuevo_id, **trans.model_dump()}
    t_list.append(nuevo_dict)
    escribir_transformaciones(t_list)
    return nuevo_dict

@router.put("/{trans_id}", response_model=TransformacionResponse)
def actualizar_transformacion(trans_id: int, datos: TransformacionUpdate):
    t_list = leer_transformaciones()
    index = next((i for i, tr in enumerate(t_list) if tr["id"] == trans_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail=f"No se encontró la transformación con ID {trans_id}")
    
    t_list[index].update(datos.model_dump(exclude_unset=True))
    escribir_transformaciones(t_list)
    return t_list[index]

@router.delete("/{trans_id}")
def eliminar_transformacion_logica(trans_id: int):
    t_list = leer_transformaciones()
    t = next((tr for tr in t_list if tr["id"] == trans_id), None)
    if not t:
        raise HTTPException(status_code=404, detail=f"No se encontró la transformación con ID {trans_id}")
    
    t["activo"] = False
    escribir_transformaciones(t_list)
    return {"status": "success", "message": f"Transformación '{t['nombre']}' desactivada (borrado lógico en transformaciones.csv)."}