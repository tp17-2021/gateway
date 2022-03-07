from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Body, Request, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_socketio import SocketManager

import os
import requests
import asyncio

import src.database as db
import src.helper
from src.auth import *

app = FastAPI(root_path=os.environ['ROOT_PATH'])
keys_db_lock = asyncio.Lock()
socket_manager = SocketManager(app=app)

async def notify_voting_terminals(status) -> dict[str, list[str]]:
    success_arr = []
    error_arr = []

    terminals = await src.helper.get_terminals()
    print(terminals)

    print("Emiting state", status)
    await app.sio.emit(
        'actual_state', {
            "state": status
        }
    )

    for terminal in terminals:
        try:
            payload = {
                'status': status
            }
            print('Sending', payload)

            terminal_endpoint = f'http://{terminal["ip"]}/backend/api/election/state'
            print('Sending data to', terminal_endpoint)

            response = requests.post(terminal_endpoint, json=payload)
            print('Response', response.status_code, response.text)

            response.raise_for_status()

            success_arr.append(terminal['_id'])

        except Exception as err:
            error_arr.append(terminal['_id'])
            print('Error', str(err))
            # todo log the error

    return {
        'success' : success_arr,
        'error' : error_arr,
    }


@app.on_event('startup')
async def startup():
    print('Deleting all keys')
    await db.keys_collection.delete_many({})
    print('Deleted all keys')

    await src.helper.insert_local_vt_if_env()


@app.get('/')
async def root () -> dict:
    """Simple hello message"""

    return {
        'status': 'success',
        'message': 'Hello from voting process manager.'
    }

@app.get('/election-config')
async def election_config () -> dict:
    """Returns necessary config fields for gateway from config"""
    
    response = requests.get(
        "http://web/statevector/config/config.json",
    )

    response = response.json()

    return {
        'status': 'success',
        'texts': response['texts']
    }


@app.get('/terminals-status')
async def election_config () -> dict:
    """Returns necessary staus information of connected voting terminals"""
    
    terminals = await src.helper.get_terminals()

    terminals_transformed = []
    for terminal in terminals:
        terminals_transformed.append({
            'id' : terminal['_id'],
            'ip_address' : terminal['ip'],
            'status' : 'active', ## TODO correct status
        })
    
    return {
        'status': 'success',
        'terminals': terminals_transformed
    }

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_dictionary, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/current-user/", response_model=User)
async def current_user(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post('/start')
async def start_voting_process (current_user: User = Depends(get_current_active_user)) -> dict:
    """Start voting from gateway and notify terminals"""
    
    requests.post('http://statevector/state_election', json='1')

    notify_status = await notify_voting_terminals('start')
    return {
        'status': 'success',
        'success_terminals' : notify_status['success'],
        'success_terminals_count' : len(notify_status['success']),
        'error_terminals' : notify_status['error'],
        'error_terminals_count' : len(notify_status['error']),
    }


@app.post('/end')
async def end_voting_process (current_user: User = Depends(get_current_active_user)) -> dict:
    """End voting from gateway and notify terminals"""

    requests.post('http://statevector/state_election', json='0')

    notify_status = await notify_voting_terminals('end')
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
