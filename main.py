try:
    from fastapi import FastAPI, HTTPException  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - handled by the runtime environment
    class FastAPI:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            raise ImportError("FastAPI is required to run this application. Install it with 'pip install fastapi'.")

    class HTTPException(Exception):  # type: ignore[no-redef]
        pass

from enum import Enum
import typing

try:
    from pydantic import BaseModel, Field  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - handled by the runtime environment
    class BaseModel:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            raise ImportError("Pydantic is required to run this application. Install it with 'pip install pydantic'.")

    class Field:  # type: ignore[no-redef]
        def __init__(self, default=..., *args, **kwargs):
            self.default = default
            self.kwargs = kwargs

        def __call__(self, *args, **kwargs):
            return self.default

app = FastAPI(
    title="Dragon Ball Z Ki Levels API",
    description="API para consultar niveles de poder y simular combates en DBZ",
    version="1.0.0"
)

class RazaEnum(str, Enum):
    SAIYAJIN = "Saiyajin"
    NAMEKIANO = "Namekiano"
    HUMANO = "Humano"
    ANDROIDE = "Androide"
    RAZA_FREEZER = "Raza de Freezer"

class PersonajeCreate(BaseModel):
    nombre: str = Field(..., example="Goku")
    raza: RazaEnum = Field(..., example=RazaEnum.SAIYAJIN)
    ki_base: int = Field(..., ge=0, example=416)
    saga_id: int = Field(..., example=1)


db_personajes = []


@app.post("/personajes", tags=["Personajes"])
def crear_personaje(personaje: PersonajeCreate):
    """Caso de uso: Registrar un nuevo personaje."""
    nuevo_id = len(db_personajes) + 1
    nuevo_personaje = {"id": nuevo_id, **personaje.model_dump()}
    db_personajes.append(nuevo_personaje)
    return {"status": "created", "data": nuevo_personaje}

class SimulacionPeleaRequest(BaseModel):
    personaje_atacante_id: int = Field(..., example=1, description="ID de Goku (1)")
    multiplicador_atacante: float = Field(default=1.0, ge=1.0, example=8.0, description="Ejemplo: Kaio-ken x8")
    personaje_defensor_id: int = Field(..., example=2, description="ID de Vegeta (2)")
    multiplicador_defensor: float = Field(default=1.0, ge=1.0, example=1.0)

class ResultadoPeleaResponse(BaseModel):
    ganador_nombre: str
    ki_efectivo_atacante: int
    ki_efectivo_defensor: int
    diferencia_ki: int
    rastreador_explota: bool
    mensaje_combate: str
