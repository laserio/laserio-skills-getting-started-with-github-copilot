from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def restore_participants(activity_name, original_participants):
    activities[activity_name]["participants"] = original_participants[:]


def test_unregister_removes_participant_from_activity():
    # Arrange
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]
    email = "michael@mergington.edu"

    try:
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in activities[activity_name]["participants"]
        assert "daniel@mergington.edu" in activities[activity_name]["participants"]
    finally:
        restore_participants(activity_name, original_participants)


def test_unregister_returns_404_for_missing_activity():
    # Arrange
    activity_name = "Unknown Activity"
    email = "test@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_participant_is_not_signed_up():
    # Arrange
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]
    email = "missing@mergington.edu"

    try:
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Student is not signed up for this activity"
    finally:
        restore_participants(activity_name, original_participants)
