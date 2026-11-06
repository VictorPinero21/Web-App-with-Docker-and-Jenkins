import pytest
import app as app_module


class FakeCursor:
    """Imita un cursor de MySQL."""

    def __init__(self, rows):
        self.rows = rows
        self.closed = False

    def execute(self, query):
        self.query = query

    def fetchone(self):
        return self.rows[0]

    def fetchall(self):
        return self.rows

    def close(self):
        self.closed = True


class FakeConnection:
    """Imita una conexión de MySQL."""

    def __init__(self, rows=None):
        self.rows = rows if rows is not None else [(1,)]

    def cursor(self):
        return FakeCursor(self.rows)


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c


@pytest.fixture
def db_up(monkeypatch):
    """La BD responde con normalidad."""
    monkeypatch.setattr(app_module, "get_db", lambda: FakeConnection())


@pytest.fixture
def db_down(monkeypatch):
    """La BD está caída: pedir conexión lanza una excepción."""

    def boom():
        raise ConnectionError("MySQL no disponible")

    monkeypatch.setattr(app_module, "get_db", boom)