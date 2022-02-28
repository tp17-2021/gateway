import requests

from writer import writer


def main ():
    requests.post('http://token-manager/tokens/writter/delete')

    w = writer.Writer()
    w.turn_off_led()
    
    while True:
        state_write = int(requests.get('http://web/statevector/gateway/state_write.txt').text)

        if state_write:
            if not writer.ON:
                w.turn_on_led()

            response = requests.post('http://token-manager/tokens/create')
            token = response.json()['token']

            token_bytes = bytes([b for b in bytearray.fromhex(token)])
            write_successful = w.write_to_tag_and_validate(token_bytes)

            if write_successful:
                params = {'token': token}
                requests.post('http://token-manager/tokens/writter/update', params=params)

            else:
                # delete unwritten tokens
                requests.post('http://token-manager/tokens/writter/delete')

                # stop writing
                requests.post('http://token-manager/tokens/writter/deactivate')

                break

        else:
            w.turn_off_led()


if __name__ == "__main__":
    main()