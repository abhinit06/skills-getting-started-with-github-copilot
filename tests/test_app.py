import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Clean up
    client.post(f"/activities/{activity}/unregister", json={"email": email})


def test_signup_for_activity_duplicate():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404


def test_unregister_from_activity_success():
    email = "tempstudent@mergington.edu"
    activity = "Art Club"
    # First sign up
    client.post(f"/activities/{activity}/signup?email={email}")
    # Now unregister
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response.status_code == 200
    assert response.json()["message"].startswith("Unregistered")


def test_unregister_from_activity_not_registered():
    email = "notregistered@mergington.edu"
    activity = "Art Club"
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_from_activity_not_found():
    response = client.post("/activities/Nonexistent/unregister", json={"email": "test@mergington.edu"})
    assert response.status_code == 404
