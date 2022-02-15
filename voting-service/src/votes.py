import datetime

import src.database as db


async def register_vote (vote: dict) -> None:
    """ Registers the vote in Vote DB model. """

    await db.collection.insert_one({
        'vote': vote,
        'time_registered': datetime.datetime.now(),
        'synchronized': False,
    })
