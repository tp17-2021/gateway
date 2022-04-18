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
