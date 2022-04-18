from fastapi.testclient import TestClient
from unittest import mock
import os
import pytest

with mock.patch.dict(os.environ, os.environ):
    from src.main import app


@pytest.fixture
def client ():
    with TestClient(app) as c:
        with mock.patch.dict(os.environ, os.environ):
            yield c


def test_it_should_work_base_url (client):
    response = client.get("/")
    assert response.status_code == 200


def test_it_should_generate_valid_token (client):
    #generate token
    response = client.post("/tokens/create")
    token = response.json()['token']

    #validate token
    response = client.post("/tokens/validate", json={ 'token' : token })
    assert response.status_code == 200


def test_it_should_deactive_token (client):
    #generate token
    response = client.post("/tokens/create")
    token = response.json()['token']

    #deactivate token
    response = client.post("/tokens/deactivate", json={ 'token' : token })

    #validate token
    response = client.post("/tokens/validate", json={ 'token' : token })
    assert response.status_code == 403
