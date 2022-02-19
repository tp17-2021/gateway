import nest_asyncio
nest_asyncio.apply()
__import__('IPython').embed()

from fastapi import Body, FastAPI, status, HTTPException
from pydantic import ValidationError
import os

import src.tokens
import src.votes
import src.helper

from src.schemas import Vote, VotePartial


app = FastAPI(root_path=os.environ['ROOT_PATH'])


@app.get('/')
async def hello ():
    """ Sample testing endpoint """

    return {'message': 'Hello from voting service!'}


@app.post('/api/vote')
async def vote (
    token: str = Body(..., embed=True),
    vote: VotePartial = Body(..., embed=True),
):
    """ Receives vote with valid token, validates the token,
    sotres the vote and invalidates the token. """

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
async def token_validity (token: str = Body(..., embed=True)):
    """ Checks if the provided token is valid. """

    response = src.tokens.validate_token(token)

    if response.status_code == status.HTTP_200_OK:
        return {'status': 'success'}
    
    raise HTTPException(response.status_code, response.text)
