import asyncio
import requests
import random
import time
import os

import src.database as db


def get_office_id():
    return requests.get('http://web/statevector/gateway/office_id.txt').text


async def get_terminals() -> list[dict[str, str]]:
    return await db.keys_collection.find().to_list(None)


async def insert_local_vt_if_env() -> None:
    try:
        if os.environ['TEST_INSERT_VT'] == 'True':
            await db.keys_collection.insert_one({
                '_id': 'TEST_VT_ID',
                'public_key': 'TEST_VT_PUBLIC_KEY',
                'ip': os.environ["TEST_INSERT_VT_IP"],
            })

    except KeyError:
        pass


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
