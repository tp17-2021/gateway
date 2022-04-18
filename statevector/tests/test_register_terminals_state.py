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


def test_it_should_return_register_terminals_state_0 (client):
    response = client.get("/state_register_terminals")
    assert response.text == '0', "register-terminals state should be 0"


def test_it_should_change_register_terminals_state (client):
    response = client.get("/state_register_terminals")
    assert response.text == '0', "register-terminals state is not 0"

    client.post('/state_register_terminals', json="1")
    response = client.get("/state_register_terminals")
    assert response.text == '1', "register-terminals state should be 1"

    client.post('/state_register_terminals', json="0")
    response = client.get("/state_register_terminals")
    assert response.text == '0', "register-terminals state should be 0"


def test_it_should_reject_invalid_register_terminals_state (client):
    response = client.get("/state_register_terminals")
    assert response.text == '0', "register-terminals state should be 0"

    response = client.post('/state_register_terminals', json="2")
    assert response.status_code == 422,\
        "Should reject invalid register-terminals state '2'"

    response = client.post('/state_register_terminals', json="")
    assert response.status_code == 422,\
        "Should reject invalid register-terminals state (empty)"

    response = client.post('/state_register_terminals', json="A")
    assert response.status_code == 422,\
        "Should reject invalid register-terminals state 'A'"

    response = client.get("/state_register_terminals")
    assert response.text == '0', "register-terminals state should be 0"
