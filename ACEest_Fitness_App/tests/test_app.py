import pytest
from app.app import app, WORKOUTS  

# This fixture clears the workout list before each test
@pytest.fixture(autouse=True)
def clear_workouts():
    WORKOUTS.clear()

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

def test_delete_workout(client):
    # Add a workout first
    client.post("/add", data={"workout": "Squats", "duration": "12"})
    r1 = client.get("/workouts")
    data_before = r1.get_json()
    assert any(w["workout"] == "Squats" for w in data_before)

    # Delete the workout
    r2 = client.post("/delete/0", follow_redirects=True)
    assert r2.status_code == 200

    # Check it's gone
    r3 = client.get("/workouts")
    data_after = r3.get_json()
    assert all(w["workout"] != "Squats" for w in data_after)

def test_delete_invalid_index_returns_404(client):
    r = client.post("/delete/999")
    assert r.status_code == 404
