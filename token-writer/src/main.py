import requests


from writer import database as db
from writer import writer

def main ():
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
            w.write_to_tag_and_validate(token_bytes)
        
            db.collection.update_one({'token': token} , { '$set' : { 'written' : True } })



        else:
            w.turn_off_led()


if __name__ == "__main__":
    main()