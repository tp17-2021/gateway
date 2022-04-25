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


def test_it_should_get_server_key_from_web ():
    server_key = requests.get('http://web/statevector/server_key').text

    assert "-----BEGIN PUBLIC KEY-----" in server_key


def test_it_should_get_private_key_from_web ():
    my_private_key = requests.get('http://web/temporary_key_location/private_key.txt').text

    assert "-----BEGIN RSA PRIVATE KEY-----" in my_private_key
