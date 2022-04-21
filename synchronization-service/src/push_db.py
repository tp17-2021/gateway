import pymongo
import random


def main():
    # connect to mongoDB
    client = pymongo.MongoClient('127.0.0.1:8223')
    db = client['gateway-db']
    collection = db['votes']

    collection.remove({})

    for i in range(100):
        collection.insert_one({
            'vote': {
                "token": "token",
                "candidates": [
                    {
                        "candidate_id" : str(random.randint(0, 10))
                    },
                    {
                        "candidate_id" : str(random.randint(0, 10))
                    }
                ],
                "party_id": str(random.randint(0, 10)),
                "office_id": "1",
                "election_id": "1",
                },
            'time_registered': random.randint(0, 100000),
            'synchronized': random.choice([True, False]),
        })


if __name__ == '__main__':
    main()
