import asyncio
from fastapi import Body, FastAPI, status, HTTPException
import os
import requests
import datetime
import uuid

import src.database as db


app = FastAPI(root_path=os.environ['ROOT_PATH'])

def token_exists(token) -> bool:
    found_token = db.collection.count_documents({'token': token})
    return True if (found_token) else False


def generate_token() -> str:
    polling_place_id =  str(requests.get('http://web/statevector/gateway/office_id.txt').text)
    token = str(uuid.uuid4())
    token = polling_place_id + '_' + token
    return token


@app.get('/')
async def root () -> dict:
    """Simple hello message"""

    return {
        'status': 'success',
        'message': 'Hello from token manager.'
    }


@app.post('/tokens/create')
async def create_token () -> dict:
    """Create and return token"""

    token = generate_token()

    while token_exists(token):
        token = generate_token()

    db.collection.insert_one({
        'token': token,
        'created_at': datetime.datetime.now(),
    })

    return {
        'status': 'success',
        'token': token
    }


@app.post('/tokens/validate')
async def create_token (token: str = Body(..., embed=True)) -> None:
    """Validate token"""

    if not token_exists(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token'
        )


@app.delete('/tokens/delete')
async def delete_token (token: str = Body(..., embed=True)) -> None:
    """Delete token"""

    if not token_exists(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token'
        )

    db.collection.delete_one({'token': token})    