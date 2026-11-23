import os

from flask import Flask, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest


app = Flask(__name__)
REQUEST_COUNT = Counter(
    "api_http_requests_total",
    "Total de HTTP requests handled by the API",
    ("method", "endpoint", "status"),
)


@app.after_request
def record_request(response):
    if request.endpoint != "metrics":
        REQUEST_COUNT.labels(
            request.method,
            request.endpoint or "not_found",
            str(response.status_code),
        ).inc()
    return response


@app.get("/")
def index():
    return jsonify(
        service="api-fase3",
        message="API de demonstracao para Kubernetes",
        version=os.getenv("APP_VERSION", "dev"),
        instance=os.getenv("HOSTNAME", "local"),
    )


@app.get("/healthz")
def health():
    return jsonify(status="ok"), 200


@app.get("/readyz")
def ready():
    return jsonify(status="ready"), 200


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
