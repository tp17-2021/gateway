import asyncio
from random import random
from fastapi import Body, FastAPI, status, HTTPException
from fastapi_utils.tasks import repeat_every
import os
import requests
import datetime
from electiersa import electiersa

import src.database as db
from src.schemas import Vote


app = FastAPI(root_path=os.environ['ROOT_PATH'])
votes_to_synchronize = 10
synchronize_every_seconds = 60
last_synchronization = None
last_success_synchronization = None
lock = asyncio.Lock()


def get_unsychronized_votes() -> list :
    query = db.collection.find({'synchronized' : False})\
        .sort([('time_registered', 1 )] )\
        .limit(votes_to_synchronize)

    items = list(query)
    return items


async def send_unsychronized_votes(items) -> requests.Response:
    server_key = requests.get('http://web/statevector/server_key').text.replace('"', '').replace('\\n', '\n')
    my_private_key = requests.get('http://web/temporary_key_location/private_key.txt').text

    print('server_key', server_key)
    print('private_key', my_private_key)

    encrypted_votes = []
    for item in items:
        new_vote = Vote(**item['vote'])

        encrypted_vote = electiersa.encrypt_vote(
            new_vote.__dict__,
            my_private_key, server_key
        )

        encrypted_votes.append(encrypted_vote.__dict__)

    server_address = requests.get('http://web/statevector/server_address').text.replace('"', '')

    server_synch_endpoint = server_address + '/elections/vote'

    print('Sending data to', server_synch_endpoint)
    response = requests.post(server_synch_endpoint, json={
        'polling_place_id': int(
            requests.get('http://web/statevector/office_id').text.replace('"', '')
        ),
        'votes': encrypted_votes,
    })

    return response


def update_unsychronized_votes(votes) -> int:

    ids = [vote['_id'] for vote in votes]

    result = db.collection.update_many(
        {'_id': {'$in': ids}},
        {'$set': {'synchronized' : True}}
    )
    return result.modified_count


async def synchronize_votes() -> None:
    await lock.acquire()
    global last_synchronization, last_success_synchronization
    try:
        print('Start synchronization')
        erorrs_count = 0
        # get unsynchronized votes
        items = get_unsychronized_votes()

        while items and erorrs_count < 2:
            # send unsynchronized votes to server
            try:
                server_response = await send_unsychronized_votes(items)
                last_synchronization = datetime.datetime.now()
                print(server_response.text)
                server_response.raise_for_status()

                # update synchronized votes on gateway
                updated_count = update_unsychronized_votes(items)
                print('Updated', updated_count)
                last_success_synchronization = datetime.datetime.now()
                erorrs_count = 0

            except requests.exceptions.HTTPError as err:
                print('Error 2', str(err))
                erorrs_count += 1

            # repeat until no unsynchronized votes
            print('Gettings remaining votes', datetime.datetime.now())
            items = get_unsychronized_votes()

    except Exception as err:
        print('Error 1', str(err))
    finally:
        lock.release()


@app.on_event("startup")
@repeat_every(seconds=synchronize_every_seconds)  # 1 minute
async def start_synchronization() -> None:
    print('Syncronization cron started')
    if not lock.locked():
        await synchronize_votes()


def get_statistics() -> dict:
    return {
        'all_count' : db.collection.count_documents( {} ),
        'syncronized_count' : db.collection.count_documents( { 'synchronized' : True } ),
        'unsyncronized_count' : db.collection.count_documents( { 'synchronized' : False } )
    }


@app.get('/')
async def root () -> dict:
    """ Simple hello message. """

    return {
        'status': 'success',
        'message': 'Hello from synchronization service.'
    }


@app.post('/synchronize')
async def synchronize () -> dict:
    """
        Try to send local votes to server and updates local status.
        If server response is different than 200, response has status 500 with error from server.
    """

    if not lock.locked():
        await synchronize_votes()
        return {
            'status': 'success',
            'message': 'Synchronization started'
        }

    return {
        'status': 'success',
        'message': 'Synchronization already started'
    }


@app.post('/statistics')
async def statistics () -> dict:
    """
        Provide statistics of votes in gateway database. Count of synchronized and unsynchronized votes.
    """

    global last_synchronization, last_success_synchronization

    return {
        'status': 'success',
        'last_synchronization': last_synchronization,
        'last_success_synchronization': last_success_synchronization,
        'statistics': get_statistics()
    }


#
# Some testing endpoints
#

@app.post('/seed')
async def seed() -> dict:
    """ Insert 10 unsynced dummy votes into gataway local gatabase. """

    for _ in range(10):

        # generate token
        response = requests.post('http://token-manager/tokens/create').json()
        token = response['token']

        # set token to written
        resp = requests.post('http://token-manager/tokens/writter/update', {'token': token})

        #insert vote
        db.collection.insert_one({
            'vote': Vote(**{
                'token': token,
                'election_id': 'election_id',
                'party_id' : 0,
                'candidate_ids' : [
                    1, 2, 3
                ]
            }).__dict__,
            'time_registered': datetime.datetime.now(),
            'synchronized': False,
        })

        # deactivate token after insert vote
        resp = requests.post('http://token-manager/tokens/deactivate', json={'token': token})
        print(resp.text)

    return {
        'status': 'success',
    }


@app.get('/test-encrypt')
async def test_encrypt() -> dict:
    """ Get a batch of encrypted votes. """

    items = get_unsychronized_votes()

    server_key = requests.get('http://web/statevector/server_key').text.replace('"', '').replace('\\n', '\n')
    my_private_key = requests.get('http://web/temporary_key_location/private_key.txt').text

    print('Server key', server_key)
    print('My private key', my_private_key)

    encrypted_votes = []
    for item in items:
        new_vote = Vote(**item['vote'])

        encrypted_vote = electiersa.encrypt_vote(
            new_vote.__dict__,
            my_private_key, server_key
        )

        encrypted_votes.append(encrypted_vote.__dict__)

    print(encrypted_votes)
    return {
        'polling_place_id': int(requests.get('http://web/statevector/office_id').text.replace('"', '')),
        'votes': encrypted_votes,
    }
