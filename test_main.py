from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_listar_personajes():
    response = client.get("/personajes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_buscar_personaje_por_nombre():
    response = client.get("/personajes/buscar/Goku")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Goku"

def test_simulacion_pelea_rastreador_explota():
    body = {
        "personaje_atacante_id": 1,
        "multiplicador_atacante": 60.0,
        "personaje_defensor_id": 2,
        "multiplicador_defensor": 1.0
    }
    response = client.post("/simular-pelea", json=body)
    assert response.status_code == 200
    assert response.json()["rastreador_explota"] is True