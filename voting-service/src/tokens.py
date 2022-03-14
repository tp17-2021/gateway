from fastapi import HTTPException, status
import requests
import os


def validate_token (token: str) -> bool:
    """ Raises HTTPException: 403 if token is invalid. """

    try:
        requests.post(
            os.environ['TOKEN_MANAGER_URL'] + '/tokens/validate',
            json={'token': token}
        ).raise_for_status()
    
    except Exception as e:
        print('in validate_token', e)
        return False
    
    return True


def use_token (token: str) -> None:
    """ Invalidates token. """

    requests.post(
        os.environ['TOKEN_MANAGER_URL'] + '/tokens/deactivate',
        json={'token': token}
    ).raise_for_status()
