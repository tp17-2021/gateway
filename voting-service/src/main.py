from fastapi import Body, FastAPI, status, HTTPException
import os

import src.tokens
import src.votes


app = FastAPI(root_path=os.environ['ROOT_PATH'])


@app.get('/')
async def hello ():
    """ Sample testing endpoint """

    return {'message': 'Hello from voting service!'}


@app.post('/api/vote')
async def vote (
    token: str = Body(..., embed=True),
    vote: dict = Body(..., embed=True),
):
    """ Receives vote with valid token, validates the token,
    sotres the vote and invalidates the token. """

    src.tokens.validate_token(token)

    try:
        vote['token'] = token
        vote['election_id'] = src.helper.get_election_id()
        await src.votes.register_vote(vote)

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
