"""Tests de los endpoints /health (liveness) y /ready (readiness)."""


def test_health_ok(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_health_no_depende_de_la_bd(client, db_down):
    """Liveness debe responder 200 aunque la BD esté caída."""
    res = client.get("/health")
    assert res.status_code == 200


def test_ready_con_bd_arriba(client, db_up):
    res = client.get("/ready")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ready", "database": "up"}


def test_ready_con_bd_caida_devuelve_503(client, db_down):
    res = client.get("/ready")
    assert res.status_code == 503
    assert res.get_json() == {"status": "not ready", "database": "down"}


def test_ready_no_filtra_detalles_del_error(client, db_down):
    """El mensaje interno de la excepción no debe llegar al cliente."""
    res = client.get("/ready")
    assert "MySQL no disponible" not in res.get_data(as_text=True)