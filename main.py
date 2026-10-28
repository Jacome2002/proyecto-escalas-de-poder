import csv
import os
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException  # pyright: ignore[reportMissingImports]
import pydantic  # pyright: ignore[reportMissingImports]

app = FastAPI(
    title="Dragon Ball Z Ki API - CRUD CSV",
    description="API RESTful para gestión de niveles de Ki y combates en DBZ con persistencia en CSV y borrado lógico",
    version="2.0.0"
)

CSV_FILE = "personajes.csv"

# ==========================================
# 1. MODELOS DE DATOS (PYDANTIC & ENUMS)
# ==========================================

class RazaEnum(str, Enum):
    SAIYAJIN = "Saiyajin"
    NAMEKIANO = "Namekiano"
    HUMANO = "Humano"
    ANDROIDE = "Androide"
    RAZA_FREEZER = "Raza de Freezer"

# Modelo 1: Saga
class Saga(pydantic.BaseModel):
    id: int
    nombre: str
    orden_cronologico: int

# Modelo 2: Transformacion
class Transformacion(pydantic.BaseModel):
    id: int
    nombre: str
    multiplicador_ki: float

# Modelo 3: Personaje (Con campo de estado para borrado lógico/histórico)
class PersonajeBase(pydantic.BaseModel):
    nombre: str = pydantic.Field(..., example="Goku")
    raza: RazaEnum = pydantic.Field(..., example=RazaEnum.SAIYAJIN)
    ki_base: int = pydantic.Field(..., ge=0, example=416)
    saga_id: int = pydantic.Field(..., example=1)
    activo: bool = pydantic.Field(default=True, description="Campo de estado para borrado lógico (histórico)")

class PersonajeCreate(PersonajeBase):
    pass

class PersonajeUpdate(pydantic.BaseModel):
    nombre: Optional[str] = None
    raza: Optional[RazaEnum] = None
    ki_base: Optional[int] = None
    saga_id: Optional[int] = None
    activo: Optional[bool] = None

class PersonajeResponse(PersonajeBase):
    id: int

# Modelo para Simulación de Pelea
class SimulacionPeleaRequest(pydantic.BaseModel):
    personaje_atacante_id: int = pydantic.Field(..., example=1)
    multiplicador_atacante: float = pydantic.Field(default=1.0, ge=1.0, example=8.0)
    personaje_defensor_id: int = pydantic.Field(..., example=2)
    multiplicador_defensor: float = pydantic.Field(default=1.0, ge=1.0, example=1.0)

class ResultadoPeleaResponse(pydantic.BaseModel):
    ganador_nombre: str
    ki_efectivo_atacante: int
    ki_efectivo_defensor: int
    diferencia_ki: int
    rastreador_explota: bool
    mensaje_combate: str


# ==========================================
# 2. FUNCIONES HELPER PARA PERSISTENCIA EN CSV
# ==========================================

def inicializar_csv():
    """Crea el archivo CSV con datos iniciales si no existe."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "nombre", "raza", "ki_base", "saga_id", "activo"])
            writer.writerow([1, "Goku", "Saiyajin", 416, 1, True])
            writer.writerow([2, "Vegeta", "Saiyajin", 18000, 1, True])
            writer.writerow([3, "Raditz", "Saiyajin", 1500, 1, False])  # Inactivo de prueba
            writer.writerow([4, "Nappa", "Saiyajin", 4000, 1, True])

def leer_csv() -> List[dict]:
    """Lee todos los registros desde el archivo CSV."""
    inicializar_csv()
    personajes = []
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            personajes.append({
                "id": int(row["id"]),
                "nombre": row["nombre"],
                "raza": row["raza"],
                "ki_base": int(row["ki_base"]),
                "saga_id": int(row["saga_id"]),
                "activo": row["activo"].lower() in ("true", "1", "t")
            })
    return personajes

def escribir_csv(personajes: List[dict]):
    """Sobrescribe el archivo CSV con la lista actualizada de registros."""
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "nombre", "raza", "ki_base", "saga_id", "activo"])
        for p in personajes:
            writer.writerow([p["id"], p["nombre"], p["raza"], p["ki_base"], p["saga_id"], p["activo"]])


# ==========================================
# 3. ENDPOINTS DE LA API (OPERACIONES CRUD)
# ==========================================

@app.get("/personajes", response_model=List[PersonajeResponse], tags=["CRUD Personajes"])
def listar_personajes(incluir_inactivos: bool = False):
    """READ: Lista todos los personajes. Por defecto omite los inactivos (borrados lógicamente)."""
    todos = leer_csv()
    if incluir_inactivos:
        return todos
    return [p for p in todos if p["activo"]]


@app.get("/personajes/{personaje_id}", response_model=PersonajeResponse, tags=["CRUD Personajes"])
def obtener_personaje_por_id(personaje_id: int):
    """READ por ID: Retorna un personaje específico con manejo de excepciones 404."""
    personajes = leer_csv()
    personaje = next((p for p in personajes if p["id"] == personaje_id), None)
    if not personaje:
        raise HTTPException(status_code=404, detail=f"No se encontró el personaje con ID {personaje_id}")
    return personaje


@app.get("/personajes/buscar/{nombre}", response_model=PersonajeResponse, tags=["Búsquedas y Filtros"])
def buscar_personaje_por_nombre(nombre: str):
    """REQUISITO EVALUACIÓN: Búsqueda por un atributo diferente al ID (Nombre)."""
    personajes = leer_csv()
    personaje = next((p for p in personajes if p["nombre"].lower() == nombre.lower() and p["activo"]), None)
    if not personaje:
        raise HTTPException(status_code=404, detail=f"No se encontró un personaje activo llamado '{nombre}'")
    return personaje


@app.get("/personajes/filtrar/", response_model=List[PersonajeResponse], tags=["Búsquedas y Filtros"])
def filtrar_personajes_por_raza(raza: RazaEnum):
    """REQUISITO EVALUACIÓN: Endpoint para filtrar listado usando un atributo (Raza)."""
    personajes = leer_csv()
    resultado = [p for p in personajes if p["raza"] == raza and p["activo"]]
    return resultado


@app.post("/personajes", response_model=PersonajeResponse, status_code=201, tags=["CRUD Personajes"])
def crear_personaje(personaje: PersonajeCreate):
    """CREATE: Agrega un nuevo personaje y persiste inmediatamente en el CSV."""
    personajes = leer_csv()
    nuevo_id = max([p["id"] for p in personajes], default=0) + 1
    nuevo_dict = {"id": nuevo_id, **personaje.model_dump()}
    personajes.append(nuevo_dict)
    escribir_csv(personajes)
    return nuevo_dict


@app.put("/personajes/{personaje_id}", response_model=PersonajeResponse, tags=["CRUD Personajes"])
def actualizar_personaje(personaje_id: int, datos: PersonajeUpdate):
    """UPDATE: Actualiza parcialmente o totalmente un personaje en el CSV."""
    personajes = leer_csv()
    index = next((i for i, p in enumerate(personajes) if p["id"] == personaje_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail=f"No se encontró el personaje con ID {personaje_id}")
    
    # Actualizar solo los campos enviados
    datos_dict = datos.model_dump(exclude_unset=True)
    personajes[index].update(datos_dict)
    escribir_csv(personajes)
    return personajes[index]


@app.delete("/personajes/{personaje_id}", tags=["CRUD Personajes"])
def eliminar_personaje_logico(personaje_id: int):
    """DELETE LÓGICO / HISTÓRICO: En lugar de borrar del CSV, cambia 'activo' a False."""
    personajes = leer_csv()
    personaje = next((p for p in personajes if p["id"] == personaje_id), None)
    if not personaje:
        raise HTTPException(status_code=404, detail=f"No se encontró el personaje con ID {personaje_id}")
    
    personaje["activo"] = False
    escribir_csv(personajes)
    return {"status": "success", "message": f"Personaje '{personaje['nombre']}' marcado como inactivo (borrado lógico registrado en el histórico CSV)."}


# ==========================================
# 4. CASO DE USO: SIMULACIÓN DE PELEA
# ==========================================

@app.post("/simular-pelea", response_model=ResultadoPeleaResponse, tags=["Lógica de Negocio"])
def simular_pelea(solicitud: SimulacionPeleaRequest):
    """Simula combate calculando Ki efectivo y verifica si el rastreador explota (>21,000 Ki)."""
    personajes = leer_csv()
    atacante = next((p for p in personajes if p["id"] == solicitud.personaje_atacante_id and p["activo"]), None)
    if not atacante:
        raise HTTPException(status_code=404, detail="El personaje atacante no existe o está inactivo.")
        
    defensor = next((p for p in personajes if p["id"] == solicitud.personaje_defensor_id and p["activo"]), None)
    if not defensor:
        raise HTTPException(status_code=404, detail="El personaje defensor no existe o está inactivo.")

    ki_efectivo_atacante = int(atacante["ki_base"] * solicitud.multiplicador_atacante)
    ki_efectivo_defensor = int(defensor["ki_base"] * solicitud.multiplicador_defensor)

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

    return ResultadoPeleaResponse(
        ganador_nombre=ganador_nombre,
        ki_efectivo_atacante=ki_efectivo_atacante,
        ki_efectivo_defensor=ki_efectivo_defensor,
        diferencia_ki=diferencia,
        rastreador_explota=rastreador_explota,
        mensaje_combate=mensaje
    )