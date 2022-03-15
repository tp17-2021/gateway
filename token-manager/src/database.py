import pymongo
import os


client = pymongo.MongoClient(
    f'mongodb://{os.environ["TOKEN_DB_HOST"]}:{os.environ["TOKEN_DB_PORT"]}'
)

collection = client\
    [os.environ['TOKEN_DB_NAME']]\
    [os.environ['TOKEN_DB_COLLECTION']]
