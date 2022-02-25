from fastapi import Body, FastAPI, status, HTTPException, Request
import json
import os
import requests
import random
import asyncio

import src.database as db
import src.helper


app = FastAPI(root_path=os.environ['ROOT_PATH'])
keys_db_lock = asyncio.Lock()


def get_terminals():
    json_text = requests.get('http://web/statevector/gateway/terminals.txt').text
    return json.loads(json_text)


def notify_voting_terminals(status) -> dict:
    terminals = get_terminals()
    output = {
        'success' : [],
        'error' : []
    }

    for terminal in terminals:
        try:
            payload = {
                'status': status
            }

            print('Sending', payload)
            terminal_endpoint = terminal['address'] + '/api/election/state'
            print('Sending data to', terminal_endpoint)
            response = requests.post(terminal_endpoint, json=payload)
            print('Response', response.status_code, response.text)
            output['success'].append(terminal['name'])
        except Exception as err:
            output['error'].append(terminal['name'])
            print('Error', str(err))
            # todo log the error

    return output

@app.get('/')
async def root () -> dict:
    """Simple hello message"""

    return {
        'status': 'success',
        'message': 'Hello from voting process manager.'
    }

@app.post('/start')
async def start_voting_process () -> dict:
    """Start voting from gateway and notify terminals"""

    notify_status = notify_voting_terminals('start')
    return {
        'status': 'success',
        'success_terminals' : notify_status['success'],
        'success_terminals_count' : len(notify_status['success']),
        'error_terminals' : notify_status['error'],
        'error_terminals_count' : len(notify_status['error']),
    }


@app.post('/end')
async def end_voting_process () -> dict:
    """End voting from gateway and notify terminals"""

    notify_status = notify_voting_terminals('end')
    return {
        'status': 'success',
        'success_terminals' : notify_status['success'],
        'success_terminals_count' : len(notify_status['success']),
        'error_terminals' : notify_status['error'],
        'error_terminals_count' : len(notify_status['error']),
    }


@app.post('/register-vt')
async def register_vt (
    request: Request,
    public_key: str = Body(..., embed=True),
):
    """Register a voting terminal"""

    ip = request.client.host
    office_id = src.helper.get_office_id()

    await keys_db_lock.acquire()
    try:
        vt_id = await src.helper.get_unique_vt_id(office_id)

        await db.keys_collection.insert_one({
            '_id': vt_id,
            'public_key': public_key,
            'ip': ip,
        })

        my_public_key = src.helper.get_public_key()
    
    finally:
        keys_db_lock.release()

    return {
        'new_id': vt_id,
        'gateway_public_key': my_public_key,
    }
