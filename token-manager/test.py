import requests
from fastapi.testclient import TestClient
from src.main import app
import src.database as db

client = TestClient(app)


# pytest testing.py --verbose


def test_it_should_work_base_url():
    response = client.get("/")
    assert response.status_code == 200


def test_it_should_generate_valid_token():
    #generate token
    response = client.post("/tokens/create")
    token = response.json()['token']

    #validate token
    response = client.post("/tokens/validate", json={ 'token' : token })
    assert response.status_code == 200


def test_it_should_deactive_token():
    #generate token
    response = client.post("/tokens/create")
    token = response.json()['token']

    #deactivate token
    response = client.post("/tokens/deactivate", json={ 'token' : token })

    #validate token
    response = client.post("/tokens/validate", json={ 'token' : token })
    assert response.status_code == 403
