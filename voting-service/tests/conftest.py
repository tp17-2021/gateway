import pytest
import asyncio
import os
import pymongo
from electiersa import electiersa


def pytest_sessionstart(session):
    client2 = pymongo.MongoClient(
        f"{os.environ['KEYS_DB_HOST']}:{os.environ['KEYS_DB_PORT']}"
    )[os.environ["KEYS_DB_NAME"]][os.environ["KEYS_DB_COLLECTION"]]
    
    private_key, public_key = electiersa.get_rsa_key_pair()
    
    print('INSERTING VT KEYS')

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
