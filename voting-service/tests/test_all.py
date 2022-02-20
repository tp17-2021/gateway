import nest_asyncio
nest_asyncio.apply()
__import__('IPython').embed()

import requests
from fastapi.testclient import TestClient
import datetime
import time
import pytest
import motor

from unittest import mock 

from electiersa import electiersa
import os

with mock.patch.dict(os.environ, os.environ):
    from src.main import app


client = TestClient(app)


def connect_to_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"{os.environ['VOTE_DB_HOST']}:{os.environ['VOTE_DB_PORT']}"
    )
    db = client[os.environ["VOTE_DB_DB_NAME"]]
    _ = str(db)
    print(_)
    return db


def test_it_should_work_base_url():
    response = client.get("/")
    assert response.status_code == 200, "Base url not working"


@pytest.mark.asyncio
async def test_it_should_accept_valid_vote():
    response = client.post("/api/vote", json={
        'vote': {
            'party_id': 1,
            'candidate_ids': [1, 2, 3],
        },
        'token': 'valid',
    })

    assert response.status_code == 200, f'Valid vote should be accepted: {response.text}'

    db = connect_to_db()

    count = await db.votes.count_documents({
        'vote': {
            'party_id': 1,
            'candidate_ids': [1, 2, 3],
            'token': 'valid',
            'election_id': 'election_id',
        },
        'synchronized': False,
    })

    assert count == 1, "Vote not found in database"


def test_it_should_not_accept_invalid_vote():
    response = client.post("/api/vote", json={
        'vote': {
            'party_id': 'string',
            'candidate_ids': [1, 2, 3],
        },
        'token': 'valid',
    })

    assert response.status_code in range(400, 500) , "Invalid vote should not be accepted"
