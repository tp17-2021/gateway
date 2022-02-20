import pytest
import asyncio
import os
import pymongo


def pytest_sessionstart(session):
    client2 = pymongo.MongoClient(
        f"{os.environ['KEYS_DB_HOST']}:{os.environ['KEYS_DB_PORT']}"
    )[os.environ["KEYS_DB_NAME"]][os.environ["KEYS_DB_COLLECTION"]]
    
    print('DELETING KEYS DB')
    client2.delete_many({})
    print('KEYS DB DELETED')


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
