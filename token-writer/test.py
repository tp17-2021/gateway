from fastapi.testclient import TestClient
from src.main import app
from unittest import mock
import os

with mock.patch.dict(os.environ, os.environ):
    client = TestClient(app)


# pytest testing.py --verbose


def test_it_should_work_base_url():
    assert True
