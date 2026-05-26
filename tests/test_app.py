from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def restore_participants(activity_name, original_participants):
    activities[activity_name]["participants"] = original_participants[:]


def test_unregister_removes_participant_from_activity():
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]

    try:
        response = client.delete(
            f"/activities/{activity_name}/unregister?email=michael@mergington.edu"
        )

        assert response.status_code == 200
        assert response.json()["message"] == (
            "Unregistered michael@mergington.edu from Chess Club"
        )
        assert "michael@mergington.edu" not in activities[activity_name]["participants"]
        assert "daniel@mergington.edu" in activities[activity_name]["participants"]
    finally:
        restore_participants(activity_name, original_participants)


def test_unregister_returns_404_for_missing_activity():
    response = client.delete("/activities/Unknown Activity/unregister?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_participant_is_not_signed_up():
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]

    try:
        response = client.delete(
            f"/activities/{activity_name}/unregister?email=missing@mergington.edu"
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Student is not signed up for this activity"
    finally:
        restore_participants(activity_name, original_participants)
