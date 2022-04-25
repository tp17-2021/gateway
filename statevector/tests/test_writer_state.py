from fastapi.testclient import TestClient
from unittest import mock
import os
import pytest

with mock.patch.dict(os.environ, os.environ):
    from src.main import app


@pytest.fixture
def client ():
    with TestClient(app) as c:
        yield c


def test_it_should_return_write_state_0 (client):
    response = client.get("/state_write")
    assert response.text == '0', "Write state should be 0"


def test_it_should_change_write_state (client):
    response = client.get("/state_write")
    assert response.text == '0', "Write state is not 0"

    client.post('/state_write', json="1")
    response = client.get("/state_write")
    assert response.text == '1', "Write state should be 1"

    client.post('/state_write', json="0")
    response = client.get("/state_write")
    assert response.text == '0', "Write state should be 0"


def test_it_should_reject_invalid_write_state (client):
    response = client.get("/state_write")
    assert response.text == '0', "Write state should be 0"

    response = client.post('/state_write', json="2")
    assert response.status_code == 422,\
        "Should reject invalid write state '2'"

    response = client.post('/state_write', json="")
    assert response.status_code == 422,\
        "Should reject invalid write state (empty)"

    response = client.post('/state_write', json="A")
    assert response.status_code == 422,\
        "Should reject invalid write state 'A'"

    response = client.get("/state_write")
    assert response.text == '0', "Write state should be 0"
