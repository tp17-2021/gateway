from pickle import FALSE
from time import time
from fastapi import Body, FastAPI, status, HTTPException
import os
import requests
import datetime
import uuid
import re

import src.database as db
import src.writer.writer as writer


app = FastAPI(root_path=os.environ['ROOT_PATH'])

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


@app.get('/')
async def root () -> dict:
    """Simple hello message"""

    return {
        'status': 'success',
        'message': 'Hello from token manager.'
    }


@app.post('/tokens/state/deactivate')
async def deactivate_state ():
    data = '0'
    response = requests.put('http://web/statevector/gateway/state_write.txt', data=data)
    return response.text


@app.post('/tokens/state/activate')
async def activate_state ():
    data = '1'
    response = requests.put('http://web/statevector/gateway/state_write.txt', data=data)
    return response.text


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