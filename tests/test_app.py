from app import app


def test_index_returns_service_information():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert response.json["service"] == "api-fase3"
    assert "version" in response.json
    assert "instance" in response.json


def test_health_and_readiness_probes():
    client = app.test_client()

    assert client.get("/healthz").json == {"status": "ok"}
    assert client.get("/readyz").json == {"status": "ready"}


def test_metrics_endpoint_exposes_request_counter():
    client = app.test_client()
    client.get("/")

    response = client.get("/metrics")

    assert response.status_code == 200
    assert b"api_http_requests_total" in response.data
