import pytest
import asyncio
import os
import pymongo
from electiersa import electiersa


def pytest_sessionstart(session):
    print('DELETING VOTE DB')
    
    client = pymongo.MongoClient(
        f"{os.environ['VOTE_DB_HOST']}:{os.environ['VOTE_DB_PORT']}"
    )[os.environ["VOTE_DB_DB_NAME"]][os.environ["VOTE_DB_COLLECTION"]]
    
    client.delete_many({})

    print('VOTE DB DELETED')

    print('INDERTING VT KEYS')
    
    client2 = pymongo.MongoClient(
        f"{os.environ['KEYS_DB_HOST']}:{os.environ['KEYS_DB_PORT']}"
    )[os.environ["KEYS_DB_NAME"]][os.environ["KEYS_DB_COLLECTION"]]
    
    print('DELETING KEYS DB')
    client2.delete_many({})
    print('KEYS DB DELETED')

    private_key, public_key = electiersa.get_rsa_key_pair()

    client2.insert_one({
        '_id': 'test',
        'public_key': public_key,
        'ip': 'none',
        'private_key_for_testing': private_key,
    })

    print('VT KEYS INSERTED')


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
