import asyncio
import os
import requests
import time

from writer import writer

async def delete_unwritten_tokens():
    while True:
        try:
            requests.post(
                f'http://{os.environ["TOKEN_MANAGER_PATH"]}/tokens/writter/delete',
                json={'event': 'restart'}
            )
            break
        except requests.exceptions.ConnectionError:
            await asyncio.sleep(1)


async def loop(writer):
    while True:
        try:
            state_write = int(requests.get(
                f'http://{os.environ["STATEVECTOR_PATH"]}/state_write').text)
            if state_write:
                writer.start_writing()

            else:
                writer.stop_writing()

        except ValueError:
            print('Probablu can not connect to statevector')

        finally:
            await asyncio.sleep(1)


async def main():
    w = writer.Writer()
    await w.set_led_status(False)
    asyncio.ensure_future(loop(w))
    await delete_unwritten_tokens()

    last_written_value = b''
    last_write_time = 0

    while True:
        await w.set_led_status(False)
        if not w.can_write:
            await asyncio.sleep(.1)
            continue

        bdata: bytes = await w.wait_for_tag_read()
        if not bdata:
            continue

        # down allowing to write the same value to the tag twice before 60 seconds
        if last_written_value == bdata and last_write_time + 30 > time.time():
            print(
                "Value to write is the same as last written value, " +
                "skipping (30 second cooldown)"
            )
            await asyncio.sleep(.1)
            continue

        got_token = bdata.hex()
        requests.post(
            f'http://{os.environ["TOKEN_MANAGER_PATH"]}/tokens/deactivate',
            json={'token': got_token}
        )

        response = requests.post(f'http://{os.environ["TOKEN_MANAGER_PATH"]}/tokens/create')
        token = response.json()['token']

        token_bytes = bytes([b for b in bytearray.fromhex(token)])
        write_successful = await w.write_to_tag_and_validate(token_bytes)
        if write_successful:
            last_written_value = token_bytes
            last_write_time = time.time()
            params = {'token': token}
            asyncio.ensure_future(w.blink_led(10))
            requests.post(f'http://{os.environ["TOKEN_MANAGER_PATH"]}/tokens/writter/update', params=params)

        else:
            requests.post(
                f'http://{os.environ["TOKEN_MANAGER_PATH"]}/tokens/writter/delete',
                json={'event': 'write_error'}
            )
            continue


if __name__ == "__main__":
    asyncio.run(main())
