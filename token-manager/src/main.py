from pickle import FALSE
from time import time
from fastapi import Body, FastAPI, status, HTTPException
from fastapi_socketio import SocketManager
import os
import requests
import datetime
import uuid
import re

import src.database as db


app = FastAPI(root_path=os.environ['ROOT_PATH'])

socket_manager = SocketManager(app=app)


def token_exists(token, active=True) -> bool:
    if os.environ['ACCEPT_VALID_TOKEN'] == '1' and token == 'valid':
        print('Received development token')
        return True

    found_token = db.collection.count_documents({'token': token, 'active': active})
    return True if (found_token) else False


def generate_token() -> str:
    token = str(uuid.uuid4())
    token = re.sub(r"-", "", token)
    return token


@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    state_write = int(requests.get('http://web/statevector/gateway/state_write.txt').text)

    await app.sio.emit(
        'writer_status', {
            'status' : 'idle' if state_write else 'off',
        }
    )

@app.get('/')
async def root () -> dict:
    """Simple hello message"""

    return {
        'status': 'success',
        'message': 'Hello from token manager.'
    }


@app.post('/tokens/writter/activate')
async def activate_state () -> dict:
    """
    Activate NFC writter machine. After turning on, machine's led will turn on
    and be able to write data to NFC tokens.
    """
    requests.put('http://web/statevector/gateway/state_write.txt', data='1')

    await app.sio.emit(
        'writer_status', {
            'status' : 'idle'
        }
    )

    return {
        'status': 'success',
        'message': 'NFC writter machine was activated.'
    }


@app.post('/tokens/writter/deactivate')
async def deactivate_state () -> dict:
    """
    Deactivate NFC writter machine. 1 NFC token lefts to be activated, after
    that NFC wrtter machine will turn off and not be able to write any kind
    of data to NFC token.
    """

    requests.put('http://web/statevector/gateway/state_write.txt', data='0')

    await app.sio.emit(
        'writer_status', {
            'status' : 'off'
        }
    )

    return {
        'status': 'success',
        'message': 'NFC writter machine was deactivated.'
    }


@app.post('/tokens/writter/delete')
async def delete_unwritten (
    event: str=Body(..., example='restart', embed=True)
) -> dict:
    """Delete unwritten NFC tokens from database"""
        
    db.collection.delete_many({'written': False})
        
    if event == 'write_error':
        await app.sio.emit(
            'writer_status', {
                'status' : 'error'
            }
        )

        await app.sio.sleep(1)

    await app.sio.emit(
        'writer_status', {
            'status' : 'idle'
        }
    )

    return {
        'status': 'success',
        'message': 'Unwritten NFC tokens successfully deleted from database.'
    }


@app.post('/tokens/writter/update')
async def update_written (token) -> dict:
    """Update NFC token state from unwritten to written"""

    db.collection.update_one({'token': token} , { '$set' : { 'written' : True } })

    await app.sio.emit(
        'writer_status', {
            'status' : 'success'
        }
    )

    await app.sio.sleep(1)

    await app.sio.emit(
        'writer_status', {
            'status' : 'idle'
        }
    )

    return {
        'status': 'success',
        'message': 'Updated NFC tokens successfully.'
    }


@app.post('/tokens/create')
async def create_token () -> dict:
    """Create and return token"""

    token = generate_token()

    while token_exists(token):
        token = generate_token()

    print(token)
    db.collection.insert_one({
        'token': token,
        'active': True,
        'written': False,
        'created_at': datetime.datetime.now(),
    })

    return {
        'status': 'success',
        'token': token
    }

@app.post('/tokens/validate')
async def validate_token (token: str = Body(..., embed=True)) -> None:
    """Validate token"""

    if not token_exists(token, active=True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token'
        )


@app.post('/tokens/deactivate')
async def deactivate_token (token: str = Body(..., embed=True)) -> None:
    """Deactive token -> change active status to false"""

    if not token_exists(token, active=True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token'
        )

    db.collection.update_one({'token': token} , { '$set' : { 'active' : False } })



@app.delete('/tokens/delete')
async def delete_token (token: str = Body(..., embed=True)) -> None:
    """Delete token"""

    if not token_exists(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token'
        )

    db.collection.delete_one({'token': token})