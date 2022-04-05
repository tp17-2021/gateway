from asyncio import events
from datetime import datetime, timedelta
import sys
import subprocess
from typing import Optional
from unittest import result
from urllib import response
from click import command

from fastapi import Depends, Body, Request, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_socketio import SocketManager
from starlette.responses import JSONResponse


import os
import re
import time
import requests
import asyncio
import datetime
import base64

from electiersa import electiersa

from src import schemas
import src.database as db
import src.helper
from src.auth import *

app = FastAPI(root_path=os.environ['ROOT_PATH'])
keys_db_lock = asyncio.Lock()
socket_manager = SocketManager(app=app)

@app.sio.on('connect')
async def ws_handle_join(sid, *args, **kwargs):
    print("WS VT connected", sid)

@app.sio.on('disconnect')
async def ws_handle_leave(sid, *args, **kwargs):
    print("WS VT disconnected", sid)
    update_terminal_status(sid, 'disconnected')

@app.sio.on('vt_stauts')
async def ws_handle_vt_stauts(sid, *args, **kwargs):
    data = args[0]
    print(data)
    terminal_id = data['vt_id']
    terminal_status = data['status']
    set_terminal_sid(terminal_id, sid)
    update_terminal_status(sid, terminal_status)
    print('WS vt_status', sid)


def update_terminal_status(terminal_sid, terminal_status):
    db.keys_collection.update_one({'terminal_sid': terminal_sid} , { '$set' : { 'status' : terminal_status, 'updated_at' : datetime.now() } })

def set_terminal_sid(terminal_id, terminal_sid):
    db.keys_collection.update_one({'_id': terminal_id} , { '$set' : { 'terminal_sid' : terminal_sid } })

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
async def terminals_status (current_user: User = Depends(get_current_active_user)) -> dict:
    """Returns necessary staus information of connected voting terminals"""

    terminals = await src.helper.get_terminals()

    terminals_transformed = []
    for terminal in terminals:
        terminals_transformed.append({
            'id' : terminal['_id'],
            'ip_address' : terminal['ip'],
            'updated_at' : terminal['updated_at'] if 'updated_at' in terminal else None,
            'status' : terminal['status'] if 'status' in terminal else None
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

    if(src.helper.check_election_state_running()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election is already running",
        )

    requests.post('http://statevector/state_election', json='1')

    notify_status = await notify_voting_terminals('start')

    # insert election started event
    await db.events_collection.insert_one({
        'action': 'elections_started',
        'created_at': datetime.now()
    })

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

    if(not src.helper.check_election_state_running()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election is already stopped",
        )

    requests.post('http://statevector/state_election', json='0')

    # insert election ended event
    await db.events_collection.insert_one({
        'action': 'elections_stopped',
        'created_at': datetime.now()
    })

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

@app.get('/gateway-elections-events')
async def gateway_events (current_user: User = Depends(get_current_active_user)) -> dict:
    """Get gateway events"""

    query = db.events_collection.find({'action': {'$in': ['elections_started', 'elections_stopped']}}, {'_id': 0}).sort('created_at', -1)
    events = [i async for i in query]

    return {
        'status': 'success',
        'events' : events,
    }

@app.get('/gateway-elections-events/first-start')
async def get_first_start (current_user: User = Depends(get_current_active_user)) -> dict:
    """Get first start"""

    query = db.events_collection.find({'action': 'elections_started'}, {'_id': 0}).sort('created_at', 1).limit(1)
    start = [i async for i in query]
    start = start[0] if len(start) > 0 else None

    return {
        'status': 'success',
        'first_start' : start,
    }

@app.get('/gateway-elections-events/last-end')
async def get_last_end (current_user: User = Depends(get_current_active_user)) -> dict:
    """Get last end"""

    query = db.events_collection.find({'action': 'elections_stopped'}, {'_id': 0}).sort('created_at', 1).limit(1)
    end = [i async for i in query]
    end = end[0] if len(end) > 0 else None

    return {
        'status': 'success',
        'last_end' : end,
    }


### Election report
@app.post('/commission-paper/generate')
async def generate_commission_paper(request: schemas.CommissionPaper):
    """
    Generate commission paper in pdf format encoded in base64 and store it into database
    """
    
    parties, candidates, polling_place = src.helper.get_config()

    registered_voters_count = str(polling_place["registered_voters_count"])
    participated_voters_count = str(await db.keys_client['gateway-db']['votes'].count_documents({}))
    participated_voters_percentage = format(round(int(participated_voters_count) / int(registered_voters_count), 2), ".2f")

    table_polling_place = src.helper.fill_table_polling_place(polling_place)
    table_parties = await src.helper.fill_table_parties(parties, polling_place)
    table_candidates = await src.helper.fill_table_candidates(parties, candidates, polling_place)

    participated_members = str(len(request.participated_members)+1)
    table_president = src.helper.fill_table_president(request.president)
    table_members = src.helper.fill_table_members(request.participated_members)
    table_events = await src.helper.fill_table_events()

    # date_and_time = time.strftime("%d.%m.%Y %H:%M:%S")
    date_and_time = str(datetime.now())
    
    date = time.strftime("%d.%m.%Y")

    with open("src/template.md", "r", encoding="utf-8") as file:
        text = file.read()
        text = re.sub(r"REGISTERED_VOTERS_COUNT", registered_voters_count, text)
        text = re.sub(r"PARTICIPATED_VOTERS_COUNT", participated_voters_count, text)
        text = re.sub(r"PARTICIPATED_VOTERS_PERCENTAGE", participated_voters_percentage, text)
        text = re.sub(r"TABLE_POLLING_PLACE", table_polling_place, text)
        text = re.sub(r"TABLE_PARTIES", table_parties, text)
        text = re.sub(r"TABLE_CANDIDATES", table_candidates, text)
        text = re.sub(r"PARTICIPATED_MEMBERS_COUNT", participated_members, text)
        text = re.sub(r"TABLE_PRESIDENT", table_president, text)
        text = re.sub(r"TABLE_MEMBERS", table_members, text)
        text = re.sub(r"TABLE_EVENTS", table_events, text)
        text = re.sub(r"DATE_AND_TIME", date_and_time, text)
        text = re.sub(r"DATE", date, text)

    with open("src/output.md", "w", encoding="utf-8") as file:
        file.write(text)

    command = "pandoc -t html --pdf-engine-opt=--enable-local-file-access --css src/output.css src/output.md -o src/output.pdf"
    subprocess.run(command, shell=True, check=True)

    with open("src/output.pdf", "rb") as pdf_file:
        data = base64.b64encode(pdf_file.read())
        # return data

        db.keys_client['gateway-db']['commission_papers'].drop({})
        db.keys_client['gateway-db']['commission_papers'].insert_one({
            "data": data
        })

        return {
            'status': 'success',
            'message': 'Commission paper was successfully generated.'
        }

@app.get('/commission-paper')
async def get_commission_paper():
    """
    Get commission paper from database encoded in base64
    """

    query = db.keys_client['gateway-db']['commission_papers'].find({}, {"_id": 0}).limit(1)
    commission_paper = [i async for i in query][0]
    data = commission_paper["data"]
    return {
        'status': 'success',
        'data': data
    }


@app.post('/commission-paper/send')
async def send_commission_paper():
    """
    Send commission paper to server
    """

    query = db.keys_client['gateway-db']['commission_papers'].find({}, {"_id": 0, "data": 1}).limit(1)
    result = [document async for document in query][0]

    date_and_time = time.strftime("%d.%m.%Y %H:%M:%S")
    polling_place_id = int(src.helper.get_office_id())
    commission_paper = {
        "data": result["data"].decode("utf-8")
    }

    server_key = requests.get('http://web/statevector/server_key').text.replace('"', '').replace('\\n', '\n')
    my_private_key = requests.get('http://web/temporary_key_location/private_key.txt').text

    encrypted_commission_paper = electiersa.encrypt_vote(commission_paper, my_private_key, server_key)

    headers = {
        "accept": "application/json",
    }

    payload = {
        "date_and_time": date_and_time,
        "polling_place_id": polling_place_id,
        "encrypted_commission_paper": encrypted_commission_paper.__dict__,
    }

    # fiit server
    response = requests.post("https://team17-21.studenti.fiit.stuba.sk/server/database/commission-paper", headers=headers, json=payload)
    
    # local server
    # response = requests.post("http://host.docker.internal:8222/database/commission-paper", headers=headers, json=payload)
    
    if response.status_code == 200:
        return {
            'status': 'success',
            'message': 'Commission paper was successfully sent to server'
        }
    else:
        return {
            'status': 'failure',
            'message': response.text
        }