"""Tests del resto de rutas."""
import app as app_module
from conftest import FakeConnection


def test_get_table_devuelve_las_tablas(client, monkeypatch):
    conn = FakeConnection(rows=[("users",), ("orders",)])
    monkeypatch.setattr(app_module, "get_db", lambda: conn)

    res = client.get("/getTable")

    assert res.status_code == 200
    assert res.get_json() == {"tables": ["users", "orders"]}


def test_version_usa_la_variable_de_entorno(client, monkeypatch):
    monkeypatch.setattr(app_module, "version_value", "1.2.3")
    res = client.get("/version")
    assert res.get_json() == {"version": "1.2.3"}


def test_index_renderiza_la_plantilla(client):
    """También sirve de regresión del error TemplateNotFound."""
    res = client.get("/")
    assert res.status_code == 200