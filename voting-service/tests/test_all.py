import nest_asyncio
nest_asyncio.apply()
__import__('IPython').embed()

import requests
from fastapi.testclient import TestClient
import pytest
import motor

from unittest import mock 

from electiersa import electiersa
import os

with mock.patch.dict(os.environ, os.environ):
    from src.main import app


client = TestClient(app)


def connect_to_db(name: str='VOTE'):
    if name == 'VOTE':
        client = motor.motor_asyncio.AsyncIOMotorClient(
            f"{os.environ['VOTE_DB_HOST']}:{os.environ['VOTE_DB_PORT']}"
        )
        db = client[os.environ["VOTE_DB_DB_NAME"]][os.environ["VOTE_DB_COLLECTION"]]
        _ = str(db)
        print(_)
        return db

    if name == 'KEYS':
        client = motor.motor_asyncio.AsyncIOMotorClient(
            f"{os.environ['KEYS_DB_HOST']}:{os.environ['KEYS_DB_PORT']}"
        )
        db = client[os.environ["KEYS_DB_NAME"]][os.environ["KEYS_DB_COLLECTION"]]
        _ = str(db)
        print(_)
        return db

    raise Exception(f'Unknown database name: {name}')


def set_election_state(state: str):
    requests.put('http://web/statevector/gateway/state_election.txt', data=state)
    

def test_it_should_work_base_url():
    response = client.get("/")
    assert response.status_code == 200, "Base url not working"


@pytest.mark.asyncio
async def test_it_should_accept_valid_vote():
    set_election_state('1')
    
    data = {
        'vote': {
            'party_id': 1,
            'candidate_ids': [1, 2, 3],
        },
        'token': 'valid',
    }

    g_public_key = requests.get('http://web/temporary_key_location/public_key.txt').text
    vt_private_key = await connect_to_db('KEYS').find_one({'_id': 'test'})
    vt_private_key = vt_private_key['private_key_for_testing']
    voting_terminal_id = 'test'
    
    encrypted_data = electiersa.encrypt_vote(data, vt_private_key, g_public_key)

    response = client.post("/api/vote", json={
        'voting_terminal_id': voting_terminal_id,
        'payload': encrypted_data.__dict__,
    })

    assert response.status_code == 200, f'Valid vote should be accepted: {response.text}'

    count = await connect_to_db().count_documents({
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
    set_election_state('1')
    
    response = client.post("/api/vote", json={
        'vote': {
            'party_id': 'string',
            'candidate_ids': [1, 2, 3],
        },
        'token': 'valid',
    })

    assert response.status_code == 422, "Invalid vote should not be accepted"


@pytest.mark.asyncio
async def test_it_should_reject_when_not_running():
    set_election_state('0')
    
    data = {
        'vote': {
            'party_id': 1,
            'candidate_ids': [1, 2, 3],
        },
        'token': 'valid',
    }

    g_public_key = requests.get('http://web/temporary_key_location/public_key.txt').text
    vt_private_key = await connect_to_db('KEYS').find_one({'_id': 'test'})
    vt_private_key = vt_private_key['private_key_for_testing']
    voting_terminal_id = 'test'
    
    encrypted_data = electiersa.encrypt_vote(data, vt_private_key, g_public_key)

    response = client.post("/api/vote", json={
        'voting_terminal_id': voting_terminal_id,
        'payload': encrypted_data.__dict__,
    })

    assert response.status_code == 409, "Vote should not be accepted when election not running"