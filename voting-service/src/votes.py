import datetime

import src.database as db
import src.schemas.vote as Vote


async def register_vote (vote: Vote) -> None:
    """ Registers the vote in Vote DB model. """

    await db.collection.insert_one({
        'vote': vote,
        'time_registered': datetime.datetime.now(),
        'synchronized': False,
    })
