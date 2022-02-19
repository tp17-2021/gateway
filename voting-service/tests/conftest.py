import pytest
import asyncio
import os
import motor.motor_asyncio


def connect_to_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"{os.environ['VOTE_DB_HOST']}:{os.environ['VOTE_DB_PORT']}"
    )
    db = client[os.environ["VOTE_DB_DB_NAME"]]
    _ = str(db)
    print(_)
    return db


def pytest_sessionstart(session):
    print('DELETING DB')
    
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"{os.environ['VOTE_DB_HOST']}:{os.environ['VOTE_DB_PORT']}"
    )[os.environ["VOTE_DB_DB_NAME"]]
    
    client.votes.delete_many({})

    print('DB DELETED')


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
