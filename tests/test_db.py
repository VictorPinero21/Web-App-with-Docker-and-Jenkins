"""Tests del módulo db: el pool se crea bajo demanda y se recupera."""
import pytest
import db


@pytest.fixture(autouse=True)
def reset_pool(monkeypatch):
    """Cada test empieza sin pool y con variables de entorno de prueba."""
    monkeypatch.setattr(db, "_pool", None)
    monkeypatch.setenv("DB_USER", "test")
    monkeypatch.setenv("DB_PASSWORD", "test")
    monkeypatch.setenv("DB_NAME", "test")


def test_si_mysql_falla_el_pool_sigue_sin_crear(monkeypatch):
    def boom(**kwargs):
        raise ConnectionError("caído")

    monkeypatch.setattr(db.pooling, "MySQLConnectionPool", boom)

    with pytest.raises(ConnectionError):
        db.get_pool()
    assert db._pool is None


def test_el_pool_se_recupera_cuando_mysql_vuelve(monkeypatch):
    intentos = []

    def fake_pool(**kwargs):
        intentos.append(1)
        if len(intentos) == 1:
            raise ConnectionError("caído")
        return "POOL_OK"

    monkeypatch.setattr(db.pooling, "MySQLConnectionPool", fake_pool)

    with pytest.raises(ConnectionError):
        db.get_pool()          # 1.º intento: MySQL caído
    assert db.get_pool() == "POOL_OK"   # 2.º intento: ya funciona


def test_falta_variable_obligatoria(monkeypatch):
    monkeypatch.delenv("DB_PASSWORD")
    with pytest.raises(KeyError):
        db.get_pool()