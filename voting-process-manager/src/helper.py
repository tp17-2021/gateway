import requests
import random
import time

import src.database as db


def get_office_id():
    return requests.get('http://web/statevector/gateway/office_id.txt').text


async def get_unique_vt_id(office_id):
    vt_id = f'{office_id}:{random.randint(0, 1000000):06d}'
    while await db.keys_collection.count_documents({'_id': vt_id}):
        print('VT id already exists', vt_id)
        time.sleep(0.1)

        vt_id = f'{office_id}:{random.randint(0, 1000000):06d}'

    return vt_id


def get_public_key():
    key = requests.get('http://web/temporary_key_location/public_key.txt').text

    return key
