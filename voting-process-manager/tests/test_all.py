import nest_asyncio
nest_asyncio.apply()
__import__('IPython').embed()

from fastapi.testclient import TestClient
import pytest
import motor
from unittest import mock 
import os

with mock.patch.dict(os.environ, os.environ):
    from src.main import app


client = TestClient(app)


def connect_to_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"{os.environ['KEYS_DB_HOST']}:{os.environ['KEYS_DB_PORT']}"
    )
    db = client[os.environ["KEYS_DB_NAME"]][os.environ["KEYS_DB_COLLECTION"]]
    _ = str(db)
    print(_)
    return db


def test_it_should_work_base_url():
    response = client.get("/")
    assert response.status_code == 200, "Base url not working"


@pytest.mark.asyncio
async def test_it_should_accept_new_vt():
    response = client.post("/register-vt", json={
        'public_key': 'PUBLIC_KEY'
    })

    assert response.status_code == 200, f'New vt vote should be accepted: {response.text}'

    db = connect_to_db()
    count = await db.count_documents({
        '_id': response.json()['new_id'],
        'public_key': 'PUBLIC_KEY',
    })

    assert count == 1, "VT not found in database"

