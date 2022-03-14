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
    sotres the vote and invalidates the token.
    
    Returns:
        200: Vote was successfully stored
        403: Token is invalid
        409: The election is not running at the moment
        422: Invalid request body
    """

    if not src.helper.check_election_state_running():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Election is not running.'
        )

    data = await src.helper.decrypt_message(payload, voting_terminal_id)
    
    # check vote against schema
    token, vote = data['token'], VotePartial(**data['vote'])

    # chcek token
    if not src.tokens.validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token is invalid.'
        )

    try:
        new_vote = Vote(
            token=token,
            election_id=src.helper.get_election_id(),
            **vote.__dict__
        )
        
        await src.votes.register_vote(new_vote)
        
        try:
            src.tokens.use_token(token)

        except HTTPException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Failed to invalidate token after successful vote.'
            )

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post('/api/token-validity')
async def token_validity (
    voting_terminal_id: str = Body(..., embed=True),
    payload: electiersa.VoteEncrypted = Body(..., embed=True),
):
    """ Checks if the provided token is valid. """

    data = await src.helper.decrypt_message(payload, voting_terminal_id)
    
    if not src.tokens.validate_token(data['token']):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token is invalid.'
        )

    return {'status': 'success'}
