from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

# Enumeraciones
class RazaEnum(str, Enum):
    SAIYAJIN = "Saiyajin"
    NAMEKIANO = "Namekiano"
    HUMANO = "Humano"
    ANDROIDE = "Androide"
    RAZA_FREEZER = "Raza de Freezer"

# ==========================================
# MODELO 1: SAGA
# ==========================================
class SagaBase(BaseModel):
    nombre: str = Field(..., example="Saga Saiyajin")
    orden_cronologico: int = Field(..., ge=1, example=1)
    activo: bool = Field(default=True, description="Borrado lógico / Histórico")

class SagaCreate(SagaBase):
    pass

class SagaUpdate(BaseModel):
    nombre: Optional[str] = None
    orden_cronologico: Optional[int] = None
    activo: Optional[bool] = None

class SagaResponse(SagaBase):
    id: int

# ==========================================
# MODELO 2: TRANSFORMACIÓN
# ==========================================
class TransformacionBase(BaseModel):
    nombre: str = Field(..., example="Kaio-ken x4")
    multiplicador_ki: float = Field(..., ge=1.0, example=4.0)
    activo: bool = Field(default=True, description="Borrado lógico / Histórico")

class TransformacionCreate(TransformacionBase):
    pass

class TransformacionUpdate(BaseModel):
    nombre: Optional[str] = None
    multiplicador_ki: Optional[float] = None
    activo: Optional[bool] = None

class TransformacionResponse(TransformacionBase):
    id: int

# ==========================================
# MODELO 3: PERSONAJE
# ==========================================
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

# ==========================================
# MODELO 4: COMBATE 
# ==========================================
class CombateBase(BaseModel):
    personaje_atacante_id: int = Field(..., example=1)
    multiplicador_atacante: float = Field(default=1.0, ge=1.0, example=60.0)
    personaje_defensor_id: int = Field(..., example=2)
    multiplicador_defensor: float = Field(default=1.0, ge=1.0, example=1.0)
    activo: bool = Field(default=True, description="Borrado lógico / Histórico")

class CombateCreate(CombateBase):
    pass

class CombateUpdate(BaseModel):
    personaje_atacante_id: Optional[int] = Field(None, example=1)
    multiplicador_atacante: Optional[float] = Field(None, ge=1.0, example=60.0)
    personaje_defensor_id: Optional[int] = Field(None, example=2)
    multiplicador_defensor: Optional[float] = Field(None, ge=1.0, example=1.0)
    activo: Optional[bool] = None

class CombateResponse(CombateBase):
    id: int
    ganador_nombre: str
    ki_efectivo_atacante: int
    ki_efectivo_defensor: int
    diferencia_ki: int
    rastreador_explota: bool
    mensaje_combate: str