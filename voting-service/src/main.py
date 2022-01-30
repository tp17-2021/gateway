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
        await src.votes.register_vote(vote)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    src.tokens.use_token(token)


@app.post('/api/token-validity')
async def token_validity (token: str = Body(..., embed=True)):
    """ Checks if the provided token is valid. """

    src.tokens.validate_token(token)
