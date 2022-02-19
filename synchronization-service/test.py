import requests
from fastapi.testclient import TestClient
from src.main import app
import src.database as db
import datetime
import time

client = TestClient(app)


# pytest testing.py --verbose


def test_it_should_work_base_url():
    response = client.get("/")
    assert response.status_code == 200


def test_it_should_provide_statistics():
    response = client.post("/statistics")
    assert response.status_code == 200


def test_it_should_synchronize_with_server(mocker):

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


def test_it_should_get_server_key():
    server_key = requests.get('http://web/statevector/gateway/server_key.txt').text

    assert "-----BEGIN PUBLIC KEY-----" in server_key


def test_it_should_get_private_key():
    my_private_key = requests.get('http://web/temporary_key_location/private_key.txt').text

    assert "-----BEGIN RSA PRIVATE KEY-----" in my_private_key



def test_it_should_get_office_id():
    office_id = int(requests.get('http://web/statevector/gateway/office_id.txt').text)

    assert office_id == 0
