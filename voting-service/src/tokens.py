from fastapi import HTTPException, status
import requests
import os


def validate_token (token: str):
    """ Raises HTTPException: 403 if token is invalid. """

    return requests.post(
        os.environ['TOKEN_MANAGER_URL'] + '/tokens/validate',
        json={'token': token}
    )


def use_token (token: str) -> None:
    """ Invalidates token. """

    requests.post(
        os.environ['TOKEN_MANAGER_URL'] + '/tokens/deactivate',
        json={'token': token}
    ).raise_for_status()
