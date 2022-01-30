import asyncio
from fastapi import Body, FastAPI, status, HTTPException
from fastapi_utils.tasks import repeat_every
import os
import requests
import datetime

import src.database as db


app = FastAPI(root_path=os.environ['ROOT_PATH'])
votes_to_synchronize = 10
synchronize_every_seconds = 60
lock = asyncio.Lock()


def get_unsychronized_votes() -> list :
    query = db.collection.find( { 'synchronized' : False } ).sort( [('time_registered', 1 )] ).limit(votes_to_synchronize)
    items = list(query)
    return items


def send_unsychronized_votes(votes) -> requests.Response:

    serialized_votes = [vote['vote'] for vote in votes]

    payload = {
        'office_id': requests.get('http://web/statevector/gateway/office_id.txt').text,
        'data': serialized_votes,
    }

    print('Sending', payload)
    server_synch_endpoint = requests.get('http://web/statevector/gateway/server_address.txt').text + '/api/synch'
    print('Sending data to', server_synch_endpoint)
    response = requests.post(server_synch_endpoint, json=payload)
    
    return response


def update_unsychronized_votes(votes) -> int:
    
    ids = [x['_id'] for x in votes]

    result = db.collection.update_many({'_id': {'$in': ids}}, { '$set' : { 'synchronized' : True } })
    return result.modified_count


async def synchronize_votes() -> None:
    await lock.acquire()
    try:
        print('Start synchronization')
        # get unsynchronized votes
        votes = get_unsychronized_votes()
        
        while votes:
            # send unsynchronized votes to server
            try:
                server_response = send_unsychronized_votes(votes)
                server_response.raise_for_status()
            
                # update synchronized votes on gateway
                updated_count = update_unsychronized_votes(votes)

                print('Updated', updated_count)
        
            except requests.exceptions.HTTPError as err:
                print('Error 2', str(err))
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
    
    return {
        'status': 'success',
        'statistics': get_statistics() 
    }
