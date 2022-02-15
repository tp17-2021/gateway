from fastapi import Body, FastAPI, status, HTTPException, Request
import json
import os
import requests


app = FastAPI(root_path=os.environ['ROOT_PATH'])


def get_terminals():
    json_text = requests.get('http://web/statevector/gateway/terminals.txt').text
    return json.loads(json_text)


def notify_voting_terminals(status):
    terminals = get_terminals()
    for terminal in terminals:
        try:
            payload = {
                'status': status
            }

            print('Sending', payload)
            terminal_endpoint = terminal['address'] + '/api/election/config'
            print('Sending data to', terminal_endpoint)
            response = requests.post(terminal_endpoint, json=payload)
            print('Response', response.status_code, response.text)
        except Exception as err:
            print('Error', str(err))
            # todo log the error


@app.get('/')
async def root () -> dict:
    """Simple hello message"""

    return {
        'status': 'success',
        'message': 'Hello from voting process manager.'
    }

@app.post('/start')
async def start_voting_process () -> dict:
    """Start voting from gateway and notify terminals"""

    notify_voting_terminals('start')
    return {
        'status': 'success'
    }


@app.post('/end')
async def end_voting_process () -> dict:
    """End voting from gateway and notify terminals"""

    notify_voting_terminals('end')
    return {
        'status': 'success'
    }


@app.get('/register-vt')
async def register_vt (request: Request):
    """Register a voting terminal"""

    ip = request.client.host
    print(f'Registering voting terminal {ip}')

    return {
        'status': 'success'
    }
