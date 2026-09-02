from __future__ import annotations

from pathlib import Path

from app import create_app
from retention.config import Config


class TestConfig(Config):
    TESTING = True
    DATABASE_PATH = Path("/tmp/retention-test.db")


def test_home_page():
    app = create_app(TestConfig)
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Turn churn probability" in response.data


def test_health():
    app = create_app(TestConfig)
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
