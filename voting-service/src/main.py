from fastapi import Body, FastAPI, status, HTTPException
from pydantic import ValidationError
import os

import src.tokens
import src.votes
import src.helper
from src.schemas import Vote, VotePartial
from electiersa import electiersa



app = FastAPI(root_path=os.environ['ROOT_PATH'])


@app.get('/')
async def hello ():
    """ Sample testing endpoint """

    return {'message': 'Hello from voting service!'}


@app.post('/api/vote')
async def vote (
    voting_terminal_id: str = Body(..., embed=True),
    payload: electiersa.VoteEncrypted = Body(..., embed=True),
):
    """ Receives vote with valid token, validates the token,
    sotres the vote and invalidates the token. """

    data = await src.helper.decrypt_message(payload, voting_terminal_id)
    
    # check vote against schema
    token, vote = data['token'], VotePartial(**data['vote'])

    # chcek token
    src.tokens.validate_token(token)

    try:
        new_vote = Vote(
            token=token,
            election_id=src.helper.get_election_id(),
            **vote.__dict__
        )
        
        await src.votes.register_vote(new_vote)

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    try:
        src.tokens.use_token(token)

    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to invalidate token after successful vote.'
        )


@app.post('/api/token-validity')
async def token_validity (
    voting_terminal_id: str = Body(..., embed=True),
    payload: electiersa.VoteEncrypted = Body(..., embed=True),
):
    """ Checks if the provided token is valid. """

    token = await src.helper.decrypt_message(payload, voting_terminal_id)
    response = src.tokens.validate_token(token['token'])

    if response.status_code == status.HTTP_200_OK:
        return {'status': 'success'}
    
    raise HTTPException(response.status_code, response.text)
