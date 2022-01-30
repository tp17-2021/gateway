from fastapi import HTTPException, status


def validate_token (token: str) -> None:
    """ Raises HTTPException: 403 if token is invalid. """

    if token == 'valid':
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Invalid token'
    )


def use_token (token: str) -> None:
    """ Invalidates token. """

    pass
