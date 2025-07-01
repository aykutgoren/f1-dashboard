import pytest
from fastapi.testclient import TestClient

from app.main import app

# Create a TestClient instance for the FastAPI application
client = TestClient(app)


@pytest.mark.functional
def test_root() -> None:
    """
    Test the root endpoint to ensure the server is up and running.

    It checks if the response status code is 200 and the returned message
    matches the expected value.
    """
    # Send a GET request to the root endpoint
    response = client.get("/")

    # Assert that the status code is 200 OK
    assert response.status_code == 200

    # Assert that the response JSON matches the expected message
    assert response.json() == {"message": "F1 Dashboard Backend Running"}
