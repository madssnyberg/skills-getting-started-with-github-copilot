"""
Integration tests for the Mergington High School Activities API using AAA pattern.
"""

import copy
from fastapi.testclient import TestClient
from src.app import app, activities


# Make a deep copy of the original activities for test state reset
original_activities = copy.deepcopy(activities)


def reset_activities():
    """Reset activities to original state between tests."""
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


def test_get_activities():
    """Test retrieving all activities."""
    # Arrange
    reset_activities()
    client = TestClient(app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert all("participants" in activity for activity in data.values())


def test_signup_for_activity():
    """Test signing up a student for an activity."""
    # Arrange
    reset_activities()
    client = TestClient(app)
    activity_name = "Chess Club"
    initial_count = len(activities[activity_name]["participants"])
    test_email = "test.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert test_email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count + 1


def test_remove_participant():
    """Test removing a participant from an activity."""
    # Arrange
    reset_activities()
    client = TestClient(app)
    activity_name = "Chess Club"
    participant_to_remove = activities[activity_name]["participants"][0]
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{participant_to_remove}"
    )

    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    assert participant_to_remove not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count - 1


def test_root_redirect():
    """Test root endpoint redirects to static content."""
    # Arrange
    reset_activities()
    client = TestClient(app)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
