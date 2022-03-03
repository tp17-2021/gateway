import json
import requests
import time
from starlette.routing import request_response

from writer import writer


def main ():
    requests.post(
        'http://token-manager/tokens/writter/delete',
        json={'event': 'restart'}
    )

    w = writer.Writer()
    w.turn_off_led()
    
    while True:
        state_write = int(requests.get('http://web/statevector/gateway/state_write.txt').text)

        if state_write:
            if not writer.ON:
                w.turn_on_led()

            bdata: bytes = w.wait_for_tag_read()
            got_token = bdata.hex()
            requests.post(
                'http://token-manager/tokens/deactivate',
                json={'token': got_token}
            )

            response = requests.post('http://token-manager/tokens/create')
            token = response.json()['token']

            token_bytes = bytes([b for b in bytearray.fromhex(token)])
            write_successful = w.write_to_tag_and_validate(token_bytes)

            if write_successful:
                params = {'token': token}
                requests.post('http://token-manager/tokens/writter/update', params=params)
                w.blink_led(10)

            else:
                requests.post(
                    'http://token-manager/tokens/writter/delete',
                    json={'event': 'write_error'}
                )
                w.blink_led(3, speed=0.3)
                break

        else:
            w.turn_off_led()
            time.sleep(0.5)


if __name__ == "__main__":
    main()