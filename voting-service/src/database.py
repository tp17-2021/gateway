import motor.motor_asyncio
import os


vote_client = motor.motor_asyncio.AsyncIOMotorClient(
    f'{os.environ["VOTE_DB_HOST"]}:{os.environ["VOTE_DB_PORT"]}'
)

vote_collection = vote_client\
    [os.environ['VOTE_DB_DB_NAME']]\
    [os.environ['VOTE_DB_COLLECTION']]


keys_client = motor.motor_asyncio.AsyncIOMotorClient(
    f'{os.environ["KEYS_DB_HOST"]}:{os.environ["KEYS_DB_PORT"]}'
)

keys_collection = keys_client\
    [os.environ['KEYS_DB_NAME']]\
    [os.environ['KEYS_DB_COLLECTION']]
