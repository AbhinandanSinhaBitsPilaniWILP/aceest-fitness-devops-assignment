import pytest

from aceest import create_app


@pytest.fixture()
def app(tmp_path):
    return create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "aceest-test.db"),
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()


def test_health_endpoint_reports_service_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {
        "service": "aceest-fitness",
        "status": "ok",
        "version": "1.0.0",
    }


def test_home_page_is_rendered(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"ACEest Fitness" in response.data
    assert b"client-form" in response.data
    assert b"Add client" in response.data


def test_client_can_be_created_and_listed(client):
    created = client.post(
        "/api/clients",
        json={"name": "Asha Rao", "email": "asha@example.com", "goal": "Strength"},
    )

    assert created.status_code == 201
    assert created.json["client"]["name"] == "Asha Rao"
    assert created.json["client"]["goal"] == "Strength"

    listed = client.get("/api/clients")
    assert listed.status_code == 200
    assert listed.json["clients"] == [created.json["client"]]


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"email": "missing-name@example.com"}, "name and email are required"),
        ({"name": "Missing email"}, "name and email are required"),
        ({"name": "Bad email", "email": "not-an-email"}, "email must be valid"),
    ],
)
def test_client_validation_returns_a_client_error(client, payload, message):
    response = client.post("/api/clients", json=payload)

    assert response.status_code == 400
    assert response.json == {"error": message}


def test_progress_can_be_recorded_and_read_back(client):
    created = client.post(
        "/api/clients",
        json={"name": "Kabir Shah", "email": "kabir@example.com"},
    )
    client_id = created.json["client"]["id"]

    progress = client.post(
        f"/api/clients/{client_id}/progress",
        json={"weight_kg": 74.5, "workout_minutes": 45, "notes": "Good session"},
    )

    assert progress.status_code == 201
    assert progress.json["progress"]["weight_kg"] == 74.5

    detail = client.get(f"/api/clients/{client_id}")
    assert detail.status_code == 200
    assert detail.json["progress"][0]["workout_minutes"] == 45


def test_progress_validation_and_unknown_client_are_safe(client):
    missing = client.post(
        "/api/clients/999/progress",
        json={"weight_kg": 70, "workout_minutes": 30},
    )
    invalid = client.post(
        "/api/clients/999/progress",
        json={"weight_kg": -1, "workout_minutes": "thirty"},
    )

    assert missing.status_code == 404
    assert invalid.status_code == 404


def test_application_factories_can_use_isolated_databases(tmp_path):
    first = create_app({"TESTING": True, "DATABASE": str(tmp_path / "first.db")})
    second = create_app({"TESTING": True, "DATABASE": str(tmp_path / "second.db")})

    first.test_client().post(
        "/api/clients", json={"name": "Only First", "email": "first@example.com"}
    )

    assert second.test_client().get("/api/clients").json["clients"] == []

