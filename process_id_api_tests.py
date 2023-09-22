import pytest
from fastapi.testclient import TestClient
from API.process_id_api import app, ProcessManager

# Fixture to create a TestClient instance for each test
@pytest.fixture
def client():
    """Fixture to create a new TestClient for each test."""
    return TestClient(app)

def test_add_return_process_endpoint(client):
    """
    Test the endpoint for adding and returning a process.

    This test checks if a process is successfully added and then returned via the API.
    The status of the process should first be 200 (OK) when added, 
    and then 200 (OK) when it's returned.
    """
    # Add a process
    response = client.post("/processes/", json={"process_name": "test_process", "user_id": "test_user"})
    assert response.status_code == 200
    assert response.json() == {"Process_ID": 1}

    # Return the process
    response = client.put("/processes/1/test_user/test_process")
    assert response.status_code == 200
    assert response.json() == {"detail": "Process returned successfully"}

@pytest.mark.xfail(reason="Process does not belong to 'wrong_user'")
def test_return_process_wrong_user(client):
    """
    Test the endpoint for returning a process with a wrong user.

    This test should fail because the process does not belong to 'wrong_user'.
    """
    # Try to return the process with a wrong user
    response = client.put("/processes/1/wrong_user")
    assert response.status_code == 403

def test_add_process_with_empty_name(client):
    """
    Test the endpoint for adding a process with an empty name.

    This test checks if the API correctly handles the case where the process name is empty.
    """
    # Try to add a process with an empty name
    response = client.post("/processes/", json={"process_name": "", "user_id": "test_user"})
    assert response.status_code == 400
    assert response.json() == {"detail": "process_name cannot be empty"}

def test_add_process_with_empty_user_id(client):
    """
    Test the endpoint for adding a process with an empty user id.

    This test checks if the API correctly handles the case where the user id is empty.
    """
    # Try to add a process with an empty user id
    response = client.post("/processes/", json={"process_name": "test_process", "user_id": ""})
    assert response.status_code == 400

@pytest.mark.xfail(reason="Maximum number of processes has been reached")
def test_max_processes(client):
    """
    Test the endpoint for adding a process when the maximum number of processes has been reached.

    This test should fail because the maximum number of processes has already been reached.
    """
    # Try to add a process when the maximum number of processes has been reached
    response = client.post("/processes/", json={"process_name": "another_process", "user_id": "test_user"})
    assert response.status_code == 403
