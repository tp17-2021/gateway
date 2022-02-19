import datetime

import src.database as db
from src.schemas import Vote


async def register_vote (vote: Vote) -> None:
    """ Registers the vote in Vote DB model. """

    await db.collection.insert_one({
        'vote': vote.__dict__,
        'time_registered': datetime.datetime.now(),
        'synchronized': False,
    })
