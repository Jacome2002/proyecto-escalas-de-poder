import csv
import os
from typing import List

CSV_FILE = "personajes.csv"

def inicializar_csv():
    """Crea el archivo CSV inicial si no existe."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "nombre", "raza", "ki_base", "saga_id", "activo"])
            writer.writerow([1, "Goku", "Saiyajin", 416, 1, True])
            writer.writerow([2, "Vegeta", "Saiyajin", 18000, 1, True])
            writer.writerow([3, "Raditz", "Saiyajin", 1500, 1, False])
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
    """Sobrescribe el archivo CSV con los datos actualizados."""
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "nombre", "raza", "ki_base", "saga_id", "activo"])
        for p in personajes:
            writer.writerow([p["id"], p["nombre"], p["raza"], p["ki_base"], p["saga_id"], p["activo"]])