from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

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