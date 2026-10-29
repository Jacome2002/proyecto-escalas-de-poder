from fastapi import APIRouter, HTTPException
from models import SimulacionPeleaRequest, ResultadoPeleaResponse
from database import leer_personajes

router = APIRouter(
    prefix="/simular-pelea",
    tags=["Lógica de Negocio"]
)

@router.post("", response_model=ResultadoPeleaResponse)
def simular_pelea(solicitud: SimulacionPeleaRequest):
    personajes = leer_personajes()
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