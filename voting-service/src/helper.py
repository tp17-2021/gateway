from electiersa import electiersa
import requests
import src.database as db



# TODO read from config file
def get_election_id () -> str:
    """ Returns the election id of the current election. """

    return 'election_id'


def get_vt_public_key (vt_id: str) -> str:
    """ Returns the public key of the voting table with the given id. """

    key = db.keys_collection.find_one({'vt_id': vt_id})['vt_public_key']

    if not key:
        raise Exception('Key for vt: |{}| does not exist.'.format(vt_id))

    return key


def get_private_key () -> str:
    """ Returns the private key of the current election. """

    key = requests.get('http://web/temporary_key_location/private_key.txt').text
    
    return key


def decrypt_message (payload: electiersa.VoteEncrypted, vt_id: str) -> dict:
    """ Decrypts the vote and returns the token and the vote. """

    vt_public_key = get_vt_public_key(vt_id)
    g_private_key = get_private_key()

    data = electiersa.decrypt_vote(payload, g_private_key, vt_public_key)

    return data
