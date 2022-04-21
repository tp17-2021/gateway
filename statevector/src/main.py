from fastapi import FastAPI, Query, Body
import os
import asyncio


app = FastAPI(root_path=os.environ['ROOT_PATH'] if 'ROOT_PATH' in os.environ else '')

state_election_lock = asyncio.Lock()
state_election: int = 0

state_write_lock = asyncio.Lock()
state_write: int = 0

state_register_terminals_lock = asyncio.Lock()
state_register_terminals: int = 0

office_id: int = 0
pin: str = 'not set'
server_key: str = 'not set'
server_address: str = 'not set'


@app.on_event('startup')
async def startup():
    global office_id, pin, server_key, server_address

    # TODO - read from somwhere
    office_id = 0
    pin = '0000'
    server_key = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs6lvNfr+Eo6Mt+mW95fh\njUbCRygCNok8Y8yIu502lpDiz3bNdR5qRZndlq7k+8XmIv2Qm8yD9BeBJbSyvc7I\nEpRSmY1nElabMoBbU2vsPWBsu7WR31pGDtAnQYCOvofScT98lar5WY5EOIV7ZzPu\nRVtuHy/q2tD5sY2ekWJc1YsoeQ5JDK64qXHZsGaIjblm+gQemucv5TG80+sgzf7c\n2P4NpNgSJ2NT8aF/bDbu3sQk9QuQXTEnkgFxTPWCwhYzRvsyq6dSTnlbyk8xfchq\nrYj5Xnql/wcrnyOhcgeKsOBieH/fETheNm6xC6Ol9Zo0rFdtqgBDsIN6H5aPCfG4\n7QIDAQAB\n-----END PUBLIC KEY-----'
    server_address = 'https://team17-21.studenti.fiit.stuba.sk/server'

    if 'SET_OFFICE_ID' in os.environ:
        office_id = int(os.environ['SET_OFFICE_ID'])
        print('office_id set from env')

    if 'SET_PIN' in os.environ:
        pin = os.environ['SET_PIN']
        print('pin set from env')

    if 'SET_SERVER_ADDRESS' in os.environ:
        server_address = os.environ['SET_SERVER_ADDRESS']
        print('server_address set from env')

    print('Office ID:', office_id)
    print('Pin: not printing it')
    print('Server Key: ' + server_key)
    print('Server Address: ' + server_address)


@app.get('/')
async def hello ():
    """ Sample testing endpoint """

    return {'message': 'Hello from Statevector!'}


@app.get('/state_election')
async def get_state_election ():
    """ Get election state string 0 or 1 """

    global state_election, state_election_lock

    await state_election_lock.acquire()
    current_state = state_election
    state_election_lock.release()

    return current_state


# TODO - restrict access
@app.post('/state_election')
async def set_state_election (
    state: str = Body(
        ...,
        title='State',
        description='State of election. Value muste be one of 0 and 1.',
        regex='^[01]$',
        example='1',
    )
):
    """ Set election state string 0 or 1 """

    global state_election, state_election_lock

    await state_election_lock.acquire()
    state_election = int(state)
    state_election_lock.release()

    return {'message': 'Election state set to ' + state}


@app.get('/state_write')
async def get_state_write ():
    """ Get write state string 0 or 1 """
    global state_write, state_write_lock

    await state_write_lock.acquire()
    current_state = state_write
    state_write_lock.release()

    return current_state


# TODO - restrict access
@app.post('/state_write')
async def set_state_write (
    state: str = Body(
        ...,
        title='State',
        description='State of write. Value muste be one of 0 and 1.',
        regex='^[01]$',
        example='1',
    )
):
    """ Set write state string 0 or 1 """

    global state_write, state_write_lock

    await state_write_lock.acquire()
    state_write = int(state)
    state_write_lock.release()

    return {'message': 'Write state set to ' + state}

@app.get('/state_register_terminals')
async def state_register_terminals ():
    """ Get terminals registration state string 0 or 1 """
    global state_register_terminals, state_register_terminals_lock

    await state_register_terminals_lock.acquire()
    current_state = state_register_terminals
    state_register_terminals_lock.release()

    return current_state


# TODO - restrict access
@app.post('/state_register_terminals')
async def set_state_register_terminals (
    state: str = Body(
        ...,
        title='State',
        description='State of register terminals. Value muste be one of 0 and 1.',
        regex='^[01]$',
        example='1',
    )
):
    """ Set register terminals state string 0 or 1 """

    global state_register_terminals, state_register_terminals_lock

    await state_register_terminals_lock.acquire()
    state_register_terminals = int(state)
    state_register_terminals_lock.release()

    return {'message': 'Register terminals state set to ' + state}


@app.get('/office_id')
async def get_office_id ():
    """ Get office id """

    global office_id
    
    return office_id


@app.get('/pin')
async def get_pin ():
    """ Get pin """

    global pin

    return pin


@app.get('/server_key')
async def get_server_key ():
    """ Get server key """

    global server_key

    return server_key


@app.get('/server_address')
async def get_server_address ():
    """ Get server address """

    global server_address

    return server_address
