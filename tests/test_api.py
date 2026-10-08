import pytest

from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index_renders_ui(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"CI/CD Demo Calculator" in response.data


def test_info(client):
    response = client.get("/api/info")
    assert response.status_code == 200
    assert {"message", "version", "environment"} <= response.get_json().keys()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_calc_add(client):
    response = client.get("/calc/add?a=2&b=3")
    assert response.status_code == 200
    assert response.get_json()["result"] == 5


# DEMO (missing dependency): uncomment together with the power operation
def test_calc_power(client):
    response = client.get("/calc/power?a=2&b=10")
    assert response.status_code == 200
    assert response.get_json()["result"] == 1024


def test_calc_divide_by_zero(client):
    response = client.get("/calc/divide?a=1&b=0")
    assert response.status_code == 400


def test_calc_missing_params(client):
    response = client.get("/calc/add?a=1")
    assert response.status_code == 400


def test_calc_unknown_operation(client):
    response = client.get("/calc/modulo?a=2&b=3")
    assert response.status_code == 404
