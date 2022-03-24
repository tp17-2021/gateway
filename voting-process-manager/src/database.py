import motor.motor_asyncio
import os


keys_client = motor.motor_asyncio.AsyncIOMotorClient(
    f'{os.environ["KEYS_DB_HOST"]}:{os.environ["KEYS_DB_PORT"]}'
)

keys_collection = keys_client\
    [os.environ['KEYS_DB_NAME']]\
    [os.environ['KEYS_DB_COLLECTION']]

events_collection = keys_client\
    [os.environ['EVENTS_DB_NAME']]\
    [os.environ['EVENTS_DB_COLLECTION']]
