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


def test_it_should_return_election_state_0 (client):
    response = client.get("/state_election")
    assert response.text == '0', "Election state should be 0"


def test_it_should_change_election_state (client):
    response = client.get("/state_election")
    assert response.text == '0', "Election state is not 0"

    client.post('/state_election', json="1")
    response = client.get("/state_election")
    assert response.text == '1', "Election state should be 1"

    client.post('/state_election', json="0")
    response = client.get("/state_election")
    assert response.text == '0', "Election state should be 0"

def test_it_should_reject_invalid_election_state (client):
    response = client.get("/state_election")
    assert response.text == '0', "Election state should be 0"

    response = client.post('/state_election', json="2")
    assert response.status_code == 422,\
        "Should reject invalid election state '2'"

    response = client.post('/state_election', json="")
    assert response.status_code == 422,\
        "Should reject invalid election state (empty)"

    response = client.post('/state_election', json="A")
    assert response.status_code == 422,\
        "Should reject invalid election state 'A'"

    response = client.get("/state_election")
    assert response.text == '0', "Election state should be 0"
