import pymongo
import os


client = pymongo.MongoClient(
    f'mongodb://{os.environ["VOTE_DB_HOST"]}:{os.environ["VOTE_DB_PORT"]}'
)

collection = client\
    [os.environ['VOTE_DB_NAME']]\
    [os.environ['VOTE_DB_COLLECTION']]
