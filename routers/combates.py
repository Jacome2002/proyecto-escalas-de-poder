from typing import List
from fastapi import APIRouter, HTTPException
from models import CombateCreate, CombateResponse, CombateUpdate
from database import leer_personajes, leer_combates, escribir_combates

router = APIRouter(
    prefix="/combates",
    tags=["CRUD Combates (Modelo 4)"]
)

def procesar_combate_dict(combate_id: int, datos: CombateCreate) -> dict:
    """Calcula la lógica de pelea entre contendientes y genera la estructura para el CSV."""
    personajes = leer_personajes()
    atacante = next((p for p in personajes if p["id"] == datos.personaje_atacante_id and p["activo"]), None)
    if not atacante:
        raise HTTPException(status_code=404, detail=f"El personaje atacante con ID {datos.personaje_atacante_id} no existe o está inactivo.")

    defensor = next((p for p in personajes if p["id"] == datos.personaje_defensor_id and p["activo"]), None)
    if not defensor:
        raise HTTPException(status_code=404, detail=f"El personaje defensor con ID {datos.personaje_defensor_id} no existe o está inactivo.")

    ki_efectivo_atacante = int(atacante["ki_base"] * datos.multiplicador_atacante)
    ki_efectivo_defensor = int(defensor["ki_base"] * datos.multiplicador_defensor)

    if ki_efectivo_atacante >= ki_efectivo_defensor:
        ganador_nombre = atacante["nombre"]
        diferencia = ki_efectivo_atacante - ki_efectivo_defensor
    else:
        ganador_nombre = defensor["nombre"]
        diferencia = ki_efectivo_defensor - ki_efectivo_atacante

    max_ki = max(ki_efectivo_atacante, ki_efectivo_defensor)
    rastreador_explota = max_ki > 21000

    mensaje = f"¡{ganador_nombre} gana el combate con una ventaja de {diferencia:,} unidades de Ki!"
    if rastreador_explota:
        mensaje += " 💥 ¡PÍIII... BUM! El rastreador ha explotado por sobrecarga de Ki."

    return {
        "id": combate_id,
        "personaje_atacante_id": datos.personaje_atacante_id,
        "multiplicador_atacante": datos.multiplicador_atacante,
        "personaje_defensor_id": datos.personaje_defensor_id,
        "multiplicador_defensor": datos.multiplicador_defensor,
        "ganador_nombre": ganador_nombre,
        "ki_efectivo_atacante": ki_efectivo_atacante,
        "ki_efectivo_defensor": ki_efectivo_defensor,
        "diferencia_ki": diferencia,
        "rastreador_explota": rastreador_explota,
        "mensaje_combate": mensaje,
        "activo": datos.activo
    }


@router.get("", response_model=List[CombateResponse])
def listar_combates(incluir_inactivos: bool = False):
    """READ: Consulta todos los registros de combates guardados en combates.csv."""
    todos = leer_combates()
    if incluir_inactivos:
        return todos
    return [c for c in todos if c["activo"]]


@router.get("/buscar/{ganador_nombre}", response_model=List[CombateResponse])
def buscar_combates_por_ganador(ganador_nombre: str):
    """REQUISITO EVALUACIÓN: Búsqueda por atributo diferente al ID (Nombre del ganador)."""
    combates = leer_combates()
    resultado = [c for c in combates if c["ganador_nombre"].lower() == ganador_nombre.lower() and c["activo"]]
    if not resultado:
        raise HTTPException(status_code=404, detail=f"No se encontraron combates donde el ganador sea '{ganador_nombre}'")
    return resultado


@router.get("/filtrar/", response_model=List[CombateResponse])
def filtrar_combates_por_rastreador(rastreador_explota: bool):
    """REQUISITO EVALUACIÓN: Filtrado por atributo (Si el rastreador explotó o no)."""
    combates = leer_combates()
    return [c for c in combates if c["rastreador_explota"] == rastreador_explota and c["activo"]]


@router.get("/{combate_id}", response_model=CombateResponse)
def obtener_combate_por_id(combate_id: int):
    """READ por ID: Retorna un registro de combate por su ID."""
    combates = leer_combates()
    combate = next((c for c in combates if c["id"] == combate_id), None)
    if not combate:
        raise HTTPException(status_code=404, detail=f"No se encontró el combate con ID {combate_id}")
    return combate


@router.post("", response_model=CombateResponse, status_code=201)
def crear_combate(combate: CombateCreate):
    """CREATE: Simula el combate, calcula Ki efectivo y persiste el resultado en combates.csv."""
    combates = leer_combates()
    nuevo_id = max([c["id"] for c in combates], default=0) + 1
    nuevo_combate_dict = procesar_combate_dict(nuevo_id, combate)
    combates.append(nuevo_combate_dict)
    escribir_combates(combates)
    return nuevo_combate_dict


@router.put("/{combate_id}", response_model=CombateResponse)
def actualizar_combate(combate_id: int, datos: CombateUpdate):
    """UPDATE: Actualiza un registro de combate existente y recalcula los resultados en combates.csv."""
    combates = leer_combates()
    index = next((i for i, c in enumerate(combates) if c["id"] == combate_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail=f"No se encontró el combate con ID {combate_id}")

    combate_actual = combates[index]
    combate_create_updated = CombateCreate(
        personaje_atacante_id=datos.personaje_atacante_id if datos.personaje_atacante_id is not None else combate_actual["personaje_atacante_id"],
        multiplicador_atacante=datos.multiplicador_atacante if datos.multiplicador_atacante is not None else combate_actual["multiplicador_atacante"],
        personaje_defensor_id=datos.personaje_defensor_id if datos.personaje_defensor_id is not None else combate_actual["personaje_defensor_id"],
        multiplicador_defensor=datos.multiplicador_defensor if datos.multiplicador_defensor is not None else combate_actual["multiplicador_defensor"],
        activo=datos.activo if datos.activo is not None else combate_actual["activo"]
    )
    combate_recalculado = procesar_combate_dict(combate_id, combate_create_updated)
    combates[index] = combate_recalculado
    escribir_combates(combates)
    return combate_recalculado


@router.delete("/{combate_id}")
def eliminar_combate_logico(combate_id: int):
    """DELETE LÓGICO / HISTÓRICO: Cambia 'activo' a False en combates.csv sin perder el histórico."""
    combates = leer_combates()
    combate = next((c for c in combates if c["id"] == combate_id), None)
    if not combate:
        raise HTTPException(status_code=404, detail=f"No se encontró el combate con ID {combate_id}")

    combate["activo"] = False
    escribir_combates(combates)
    return {"status": "success", "message": f"Combate {combate_id} marcado como inactivo (borrado lógico registrado en combates.csv)."}