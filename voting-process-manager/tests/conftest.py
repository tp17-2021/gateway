import pytest
import asyncio
import os
import motor.motor_asyncio


def pytest_sessionstart(session):
    print('DELETING DB')
    
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"{os.environ['KEYS_DB_HOST']}:{os.environ['KEYS_DB_PORT']}"
    )[os.environ["KEYS_DB_NAME"]]
    
    client[os.environ['KEYS_DB_COLLECTION']].delete_many({})

    print('DB DELETED')


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
