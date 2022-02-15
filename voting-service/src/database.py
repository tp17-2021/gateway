import motor.motor_asyncio
import os


client = motor.motor_asyncio.AsyncIOMotorClient(
    f'{os.environ["VOTE_DB_HOST"]}:{os.environ["VOTE_DB_PORT"]}'
)

collection = client\
    [os.environ['VOTE_DB_DB_NAME']]\
    [os.environ['VOTE_DB_COLLECTION']]
