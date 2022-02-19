import asyncio
from fastapi import Body, FastAPI, status, HTTPException
from fastapi_utils.tasks import repeat_every
import os
import requests
import datetime
from electiersa import electiersa

import src.database as db


app = FastAPI(root_path=os.environ['ROOT_PATH'])
votes_to_synchronize = 10
synchronize_every_seconds = 60
last_synchronization = None
last_success_synchronization = None
lock = asyncio.Lock()


def get_unsychronized_votes() -> list :
    query = db.collection.find( { 'synchronized' : False } ).sort( [('time_registered', 1 )] ).limit(votes_to_synchronize)
    items = list(query)
    return items


async def send_unsychronized_votes(votes) -> requests.Response:

    serialized_votes = []
    server_key = requests.get('http://web/statevector/gateway/server_key.txt').text

    my_private_key = requests.get('http://web/temporary_key_location/private_key.txt').text

    for vote in votes:
        new_vote = {
            'token' : vote['vote']['token'],
            'election_id' : vote['vote']['election_id'],
            'party_id' : int(vote['vote']['party_id']),
            'candidates_ids': vote['vote']['candidates'],
        }

        new_vote = await electiersa.encrypt_vote(new_vote, my_private_key, server_key);
        serialized_votes.append(new_vote)

    payload = {
        'polling_place_id': int(requests.get('http://web/statevector/gateway/office_id.txt').text),
        'votes': serialized_votes,
    }

    server_synch_endpoint = requests.get('http://web/statevector/gateway/server_address.txt').text + '/elections/vote'
    print('Sending data to', server_synch_endpoint)
    response = requests.post(server_synch_endpoint, json=payload)
    
    return response


def update_unsychronized_votes(votes) -> int:
    
    ids = [x['_id'] for x in votes]

    result = db.collection.update_many({'_id': {'$in': ids}}, { '$set' : { 'synchronized' : True } })
    return result.modified_count


async def synchronize_votes() -> None:
    await lock.acquire()
    global last_synchronization, last_success_synchronization
    try:
        print('Start synchronization')
        erorrs_count = 0
        # get unsynchronized votes
        votes = get_unsychronized_votes()
        
        while votes and erorrs_count < 2:
            # send unsynchronized votes to server
            try:
                server_response = await send_unsychronized_votes(votes)
                last_synchronization = datetime.datetime.now();
                print(server_response.text)
                server_response.raise_for_status()
            
            
                # update synchronized votes on gateway
                updated_count = update_unsychronized_votes(votes)
                print('Updated', updated_count)
                last_success_synchronization = datetime.datetime.now();
                erorrs_count = 0
        
            except requests.exceptions.HTTPError as err:
                print('Error 2', str(err))
                erorrs_count += 1
                # todo log the error

            # repeat until no unsynchronized votes
            print('Gettings remaining votes', datetime.datetime.now())
            votes = get_unsychronized_votes()

    except Exception as err:
        print('Error 1', str(err))
        # todo log the error
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
    """Simple hello message"""

    return {
        'status': 'success',
        'message': 'Hello from synchronization service.'
    }


@app.post('/synchronize')
async def synchronize () -> dict:
    """Synchronize local votes with server"""

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
    """Get current statistics of sychnonization of local votes"""
    
    global last_synchronization, last_success_synchronization

    return {
        'status': 'success',
        'last_synchronization': last_synchronization,
        'last_success_synchronization': last_success_synchronization,
        'statistics': get_statistics() 
    }


@app.post('/seed')
async def seed() -> dict:
    # insert dummy vote
    db.collection.insert_many([{
        'vote': {
            'token': 'abcd_'+str(i),
            'election_id': 'election_id',
            'party_id' : 0, 
            'candidates' : [
                {
                    'candidate_id' : 1,
                },
                {
                    'candidate_id' : 2,
                }
            ]
        },
        'time_registered': datetime.datetime.now(),
        'synchronized': False,
    } for i in range(10)])

    return {
        'status': 'success',
    }

@app.post('/test-encrypt')
async def test_encrypt() -> dict:
    votes = get_unsychronized_votes()
    server_key = requests.get('http://web/statevector/gateway/server_key.txt').text
    serialized_votes = []

    print(server_key)
    print(votes)
    for vote in votes:
        new_vote = {
            'token' : vote['vote']['token'],
            'election_id' : vote['vote']['election_id'],
            'party_id' : int(vote['vote']['party_id']),
            'candidates_ids': [i['candidate_id'] for i in vote['vote']['candidates']],
        }

        new_vote = await electiersa.encrypt_vote(server_key, new_vote);
        serialized_votes.append(new_vote)

    print(serialized_votes)
    return {
        'polling_place_id': int(requests.get('http://web/statevector/gateway/office_id.txt').text),
        'votes': serialized_votes,
    }