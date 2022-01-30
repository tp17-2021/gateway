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