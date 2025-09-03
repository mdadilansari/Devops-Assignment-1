import pytest
from app.app import app

@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client

def test_home_page(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"ACEest Fitness" in r.data

def test_add_workout(client):
    r = client.post("/add", data={"workout": "Pushups", "duration": "10"}, follow_redirects=True)
    assert r.status_code == 200
    r2 = client.get("/workouts")
    data = r2.get_json()
    assert any(w["workout"] == "Pushups" for w in data)

def test_invalid_duration(client):
    r = client.post("/add", data={"workout": "Run", "duration": "abc"})
    assert r.status_code == 400
