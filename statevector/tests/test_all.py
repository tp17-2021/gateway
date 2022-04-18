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


def test_it_should_work_base_url (client):
    response = client.get("/")
    assert response.status_code == 200, "Base url not working"


# ---- test getters on default values

def test_it_should_return_default_office_id (client):
    response = client.get("/office_id")
    assert response.text == '42', "Default office id is wrong"


def test_it_should_return_default_server_address (client):
    response = client.get("/server_address")
    assert response.text == '"https://test.com"',\
        "Default server address is wrong"


def test_it_should_return_default_server_key (client):
    response = client.get("/server_key")
    assert response.text == '"-----BEGIN PUBLIC KEY-----\\\\ntest\\\\n-----END PUBLIC KEY-----"',\
        "Default server_key is wrong"


def test_it_should_return_default_pin (client):
    response = client.get("/pin")
    assert response.text == '"4242"', "Default pin is wrong"


# ---- test election state

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


# ---- test write state

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


# ---- test register_terminals state

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

