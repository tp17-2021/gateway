import requests
from fastapi.testclient import TestClient
import src.database as db
import datetime
import time
import pytest
from unittest import mock
import os

with mock.patch.dict(os.environ, os.environ):
    from src.main import app


@pytest.fixture
def client ():
    with TestClient(app) as c:
        yield c


def test_it_should_work_base_url (client):
    response = client.get("/")
    assert response.status_code == 200


# TODO toto by nemal byt post
def test_it_should_provide_statistics (client):
    response = client.post("/statistics")
    assert response.status_code == 200


def test_it_should_synchronize_with_server (client, mocker):
    # insert dummy vote
    db.collection.insert_many([{
        'vote': {},
        'time_registered': datetime.datetime.now(),
        'synchronized': False,
    } for _ in range(100)])

    # check if inserted
    response = client.post("/statistics")
    assert response.status_code == 200
    assert response.json()['statistics']['unsyncronized_count'] == 100

    # TODO rozmysliet, ci mockovat celu funkciu, alebo ci vieme mockovat iba request
    # tym padom by bol tento test silnejsi
    res = requests.Response()
    res.status_code = 200
    mocker.patch('src.main.send_unsychronized_votes', return_value=res)

    # call synchronization endpoint
    response = client.post("/synchronize")
    assert response.status_code == 200
    print(response.text)

    response = client.post("/synchronize")
    counter = 10
    while response.json()['message'] != 'Synchronization started' and counter:
        time.sleep(1)
        counter -=1
        response = client.post("/synchronize")

    print(counter)    

    # chceck if all synchronized
    response = client.post("/statistics")
    assert response.status_code == 200
    assert response.json()['statistics']['unsyncronized_count'] == 0
