import csv
import os
from typing import List, Dict

CSV_SAGAS = "sagas.csv"
CSV_TRANSFORMACIONES = "transformaciones.csv"
CSV_PERSONAJES = "personajes.csv"
CSV_COMBATES = "combates.csv"

def inicializar_csv():
    """Crea los 4 archivos CSV iniciales con datos semilla si no existen."""
    if not os.path.exists(CSV_SAGAS):
        with open(CSV_SAGAS, mode="w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "nombre", "orden_cronologico", "activo"])
            w.writerow([1, "Saga Saiyajin", 1, True])
            w.writerow([2, "Saga de Freezer", 2, True])
            w.writerow([3, "Saga de Cell", 3, True])

    if not os.path.exists(CSV_TRANSFORMACIONES):
        with open(CSV_TRANSFORMACIONES, mode="w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "nombre", "multiplicador_ki", "activo"])
            w.writerow([1, "Kaio-ken x2", 2.0, True])
            w.writerow([2, "Kaio-ken x4", 4.0, True])
            w.writerow([3, "Super Saiyajin", 50.0, True])

    if not os.path.exists(CSV_PERSONAJES):
        with open(CSV_PERSONAJES, mode="w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "nombre", "raza", "ki_base", "saga_id", "activo"])
            w.writerow([1, "Goku", "Saiyajin", 416, 1, True])
            w.writerow([2, "Vegeta", "Saiyajin", 18000, 1, True])
            w.writerow([3, "Raditz", "Saiyajin", 1500, 1, False])
            w.writerow([4, "Nappa", "Saiyajin", 4000, 1, True])

    if not os.path.exists(CSV_COMBATES):
        with open(CSV_COMBATES, mode="w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([
                "id", "personaje_atacante_id", "multiplicador_atacante",
                "personaje_defensor_id", "multiplicador_defensor",
                "ganador_nombre", "ki_efectivo_atacante", "ki_efectivo_defensor",
                "diferencia_ki", "rastreador_explota", "mensaje_combate", "activo"
            ])
            w.writerow([
                1, 1, 60.0, 2, 1.0,
                "Goku", 24960, 18000, 6960, True,
                "¡Goku gana el combate con una ventaja de 6,960 unidades de Ki! 💥 ¡PÍIII... BUM! El rastreador ha explotado por sobrecarga de Ki.",
                True
            ])

# --- SAGAS ---
def leer_sagas() -> List[Dict]:
    inicializar_csv()
    sagas = []
    with open(CSV_SAGAS, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sagas.append({
                "id": int(row["id"]),
                "nombre": row["nombre"],
                "orden_cronologico": int(row["orden_cronologico"]),
                "activo": row["activo"].lower() in ("true", "1", "t")
            })
    return sagas

def escribir_sagas(sagas: List[Dict]):
    with open(CSV_SAGAS, mode="w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "nombre", "orden_cronologico", "activo"])
        for s in sagas:
            w.writerow([s["id"], s["nombre"], s["orden_cronologico"], s["activo"]])

# --- TRANSFORMACIONES ---
def leer_transformaciones() -> List[Dict]:
    inicializar_csv()
    trans = []
    with open(CSV_TRANSFORMACIONES, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            trans.append({
                "id": int(row["id"]),
                "nombre": row["nombre"],
                "multiplicador_ki": float(row["multiplicador_ki"]),
                "activo": row["activo"].lower() in ("true", "1", "t")
            })
    return trans

def escribir_transformaciones(trans: List[Dict]):
    with open(CSV_TRANSFORMACIONES, mode="w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "nombre", "multiplicador_ki", "activo"])
        for t in trans:
            w.writerow([t["id"], t["nombre"], t["multiplicador_ki"], t["activo"]])

# --- PERSONAJES ---
def leer_personajes() -> List[Dict]:
    inicializar_csv()
    personajes = []
    with open(CSV_PERSONAJES, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
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

def escribir_personajes(personajes: List[Dict]):
    with open(CSV_PERSONAJES, mode="w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "nombre", "raza", "ki_base", "saga_id", "activo"])
        for p in personajes:
            w.writerow([p["id"], p["nombre"], p["raza"], p["ki_base"], p["saga_id"], p["activo"]])

# --- COMBATES ---
def leer_combates() -> List[Dict]:
    inicializar_csv()
    combates = []
    with open(CSV_COMBATES, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            combates.append({
                "id": int(row["id"]),
                "personaje_atacante_id": int(row["personaje_atacante_id"]),
                "multiplicador_atacante": float(row["multiplicador_atacante"]),
                "personaje_defensor_id": int(row["personaje_defensor_id"]),
                "multiplicador_defensor": float(row["multiplicador_defensor"]),
                "ganador_nombre": row["ganador_nombre"],
                "ki_efectivo_atacante": int(row["ki_efectivo_atacante"]),
                "ki_efectivo_defensor": int(row["ki_efectivo_defensor"]),
                "diferencia_ki": int(row["diferencia_ki"]),
                "rastreador_explota": row["rastreador_explota"].lower() in ("true", "1", "t"),
                "mensaje_combate": row["mensaje_combate"],
                "activo": row["activo"].lower() in ("true", "1", "t")
            })
    return combates

def escribir_combates(combates: List[Dict]):
    with open(CSV_COMBATES, mode="w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "id", "personaje_atacante_id", "multiplicador_atacante",
            "personaje_defensor_id", "multiplicador_defensor",
            "ganador_nombre", "ki_efectivo_atacante", "ki_efectivo_defensor",
            "diferencia_ki", "rastreador_explota", "mensaje_combate", "activo"
        ])
        for c in combates:
            w.writerow([
                c["id"], c["personaje_atacante_id"], c["multiplicador_atacante"],
                c["personaje_defensor_id"], c["multiplicador_defensor"],
                c["ganador_nombre"], c["ki_efectivo_atacante"], c["ki_efectivo_defensor"],
                c["diferencia_ki"], c["rastreador_explota"], c["mensaje_combate"], c["activo"]
            ])