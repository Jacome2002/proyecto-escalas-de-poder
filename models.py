from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class RazaEnum(str, Enum):
    SAIYAJIN = "Saiyajin"
    NAMEKIANO = "Namekiano"
    HUMANO = "Humano"
    ANDROIDE = "Androide"
    RAZA_FREEZER = "Raza de Freezer"

class Saga(BaseModel):
    id: int
    nombre: str
    orden_cronologico: int

class Transformacion(BaseModel):
    id: int
    nombre: str
    multiplicador_ki: float

class PersonajeBase(BaseModel):
    nombre: str = Field(..., example="Goku")
    raza: RazaEnum = Field(..., example=RazaEnum.SAIYAJIN)
    ki_base: int = Field(..., ge=0, example=416)
    saga_id: int = Field(..., example=1)
    activo: bool = Field(default=True, description="Borrado lógico / Histórico")

class PersonajeCreate(PersonajeBase):
    pass

class PersonajeUpdate(BaseModel):
    nombre: Optional[str] = None
    raza: Optional[RazaEnum] = None
    ki_base: Optional[int] = None
    saga_id: Optional[int] = None
    activo: Optional[bool] = None

class PersonajeResponse(PersonajeBase):
    id: int

class SimulacionPeleaRequest(BaseModel):
    personaje_atacante_id: int = Field(..., example=1)
    multiplicador_atacante: float = Field(default=1.0, ge=1.0, example=8.0)
    personaje_defensor_id: int = Field(..., example=2)
    multiplicador_defensor: float = Field(default=1.0, ge=1.0, example=1.0)

class ResultadoPeleaResponse(BaseModel):
    ganador_nombre: str
    ki_efectivo_atacante: int
    ki_efectivo_defensor: int
    diferencia_ki: int
    rastreador_explota: bool
    mensaje_combate: str