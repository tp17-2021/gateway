import usb.backend.libusb1
import usb.util
import usb.core
import struct
import random
import asyncio


def pad_bytes_with_zeros(data, length):
    return data + (length - len(data)) * b"\x00"


def create_set_report_bytes(command: bytes, data: bytes = b'') -> bytes:
    """
    command always is 2 bytes long
    data optional (can be empty)
    """
    preamble = b"\xaa\xbb"  # 2 bytes equal to 0xAABB
    device_id = b"\x00\x00"

    # 1 byte, XOR of all the bytes - device_id, self.bytes,  to Data
    CHECKSUM = b"\x00"
    CHECKSUM_ARR = device_id + command + data
    for byte in CHECKSUM_ARR:
        CHECKSUM = bytes([CHECKSUM[0] ^ byte])

    # 2 bytes, indicating the number of bytes from DeviceID to Checksum
    # the left byte is used, and the right byte is also 0x00
    LEN = struct.pack("<H", len(device_id + command + data + CHECKSUM))
    ALL = pad_bytes_with_zeros(
        preamble + LEN + device_id + command + data + CHECKSUM, 64)

    return ALL


class Writer:
    def __init__(self, usb_interface_id: int = 1, verbose: bool = False):
        self.usb_interface_id = usb_interface_id
        self.verbose = verbose
        self.can_write = True
        self.dev = None
        self.led_is_on = False

    def stop_writing(self) -> None:
        """
        Disallow writing to the writer.
        """
        self.can_write = False

    def start_writing(self) -> None:
        """
        Allow writing to the writer.
        """
        self.can_write = True

    async def connect_to_writer(self) -> None:
        print("Waiting for the writer to be connected")
        while True:
            self.dev = usb.core.find(idVendor=0x0471, idProduct=0xa112)
            if self.dev is None:
                if self.verbose:
                    print("Writer not found. Waiting for it to be connected")
                await asyncio.sleep(0.5)
            else:
                print("Successfully connected to the writer")
                # print(self.dev)
                await self.detach_kernel_driver(self.usb_interface_id)
                await self.blink_led(10, 0.05)
                break

    async def detach_kernel_driver(self, usb_interface: int) -> None:
        """
        # fixes resource busy
        # https://stackoverflow.com/questions/67453535/i-keep-getting-usb-core-usberror-errno-16-resource-busy-when-trying-to-read
        """
        try:
            if self.dev.is_kernel_driver_active(self.usb_interface_id):
                self.dev.detach_kernel_driver(self.usb_interface_id)
                if self.verbose:
                    print("Kernel driver detached to fix Resource busy error")

        except usb.core.USBError as e:
            print(
                "Could not detatch kernel driver from interface" +
                f"({self.usb_interface_id}): {str(e)}"
            )
            await asyncio.sleep(0.5)

    def set_report(
        self,
        description_type_and_index: int,
        usb_interface: int,
        data: bytes
    ) -> int:
        """
        Send set_report to the writer.
        # 0x21 = REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_OUT
        """
        SET_REPORT = 0x09
        return self.dev.ctrl_transfer(
            0x21,
            SET_REPORT,
            description_type_and_index,
            usb_interface,
            data
        )

    def get_report(
            self,
        description_type_and_index: int,
        usb_interface: int,
        max_reply_size: int
    ):
        """
        Recieve get_report from the writer.
        # 0xA1 = REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_IN
        """
        GET_REPORT = 0x01
        # max_reply_size = 64
        return self.dev.ctrl_transfer(
            0xa1,
            GET_REPORT,
            description_type_and_index,
            usb_interface,
            max_reply_size
        )

    def parse_set_report_response(self, request: bytes) -> None:
        """
        Parse set_report for debugging purposes.
        """
        request_bytes = bytes(request)
        LEN = struct.unpack("<H", request_bytes[2:4])[0]
        if self.verbose:
            print("--- Request ---")
            print("Preamble: ", request_bytes[0:2])
            print("Length:   ", request_bytes[2:4])
            print("Device ID:", request_bytes[4:6])
            print("Command:  ", request_bytes[6:8])
            print("Data:     ", request_bytes[8:8 + LEN - 5])
            print("Checksum: ", request_bytes[-1])
            print("All:", request_bytes)
            print("")

    def parse_get_report_response(self, response: bytes) -> None:
        """
        Parse get_report for debugging purposes.
        Return the data part of the response.
        """
        response_bytes = bytes(response)

        LEN = struct.unpack("<H", response_bytes[2:4])[0]

        status = response_bytes[8:9]
        DATA = response_bytes[9:9 + LEN - 5]

        if self.verbose:
            print("--- Response ---")
            print("Preamble: ", response_bytes[0:2])
            print("Length:   ", response_bytes[2:4])
            print("Device ID:", response_bytes[4:6])
            print("Command:  ", response_bytes[6:8])
            print("Status:   ", status)
            print("Data:     ", DATA)
            print("Checksum: ", response_bytes[-1])
            print("All:", response_bytes)
            print("")
            print("")
            print("")

        if status != b'\x00':
            raise ValueError(
                'Status is not 0x00, is tag placed on the writer?' +
                'Please try again - sometimes it fails'
            )

        return DATA

    async def send(self, human_title: str, command: bytes, data: bytes = b'') -> None:
        """
        Wrapper to send data to the writer and get the response in a single
        function call
        """
        if len(command) != 2:  # validation
            raise ValueError("Command must be 2 bytes long")

        while True:
            if self.dev is None:
                await self.connect_to_writer()
                await asyncio.sleep(0.5)
                continue

            try:  # try to communicate with the writer, if it is still connected
                if self.verbose:
                    print("##########", human_title, "##########")

                set_report_bytes = create_set_report_bytes(command, data)
                self.parse_set_report_response(set_report_bytes)
                response_len = self.set_report(
                    0x301, self.usb_interface_id, set_report_bytes)
                byte_array = self.get_report(
                    0x301, self.usb_interface_id, response_len)
                data = self.parse_get_report_response(byte_array)
                return data

            except usb.core.USBError:
                print("Writer was disconnected")
                await asyncio.sleep(0.5)  # fix RecursionError
                await self.connect_to_writer()

    async def set_led_status(self, is_on: bool) -> None:
        """
        Turn led on or off.
        """

        if is_on:
            COMMAND_LED_CONTROL = b"\x07\x01"
            LED_ON = b"\x01"
            await self.send("Turning on LED", COMMAND_LED_CONTROL, LED_ON)
            self.led_is_on = True

        else:
            COMMAND_LED_CONTROL = b"\x07\x01"
            LED_OFF = b"\x00"
            await self.send("Turning off LED", COMMAND_LED_CONTROL, LED_OFF)
            self.led_is_on = False

    async def blink_led(self, repeat: int = 1, speed: int = 0.2) -> None:
        """
        Blink the LED on the writer.
        repeat: number of times to blink
        """
        was_led_on = self.led_is_on
        for i in range(repeat):
            await self.set_led_status(False)
            await asyncio.sleep(speed / 2)
            await self.set_led_status(True)
            await asyncio.sleep(speed / 2)

        self.led_is_on = was_led_on

    async def get_model_string(self) -> bytes:
        """
        Get the connected model string from the writer.
        """
        COMMAND_GET_MODEL_STRING = b"\x04\x01"
        return await self.send("Getting model bytes", COMMAND_GET_MODEL_STRING)

    async def select_card_for_read_or_write(self) -> None:
        """
        Select the card nearby for read or write.
        Success if self.send() at all steps won't raise an error.
        """
        COMMAND_antena_sta = b"\x0c\x01"
        DATA = b"\x00"  # turn off RF
        await self.send("antena_sta", COMMAND_antena_sta, DATA)

        COMMAND_init_type = b"\x08\x01"
        DATA = b"\x41"
        await self.send("init_type", COMMAND_init_type, DATA)

        DATA = b"\x01"  # turn on RF
        await self.send("antena_sta", COMMAND_antena_sta, DATA)

        COMMAND_request = b"\x01\x02"
        DATA = b"\x52"
        await self.send("request", COMMAND_request, DATA)

        COMMAND_anticol = b"\x02\x02"
        DATA = b"\x04"
        CARD_SERIAL = (await self.send("anticol", COMMAND_anticol, DATA))[:-1]

        COMMAND_select = b"\x03\x02"
        await self.send("select", COMMAND_select, CARD_SERIAL)

    async def _read_from_tag(self) -> bytes:
        """
        Read the tag.
        WARNING: sometimes the tag is not read correcty.
        Use self.read_tag_with_retry() to repeat read operation until success.
        """

        await self.select_card_for_read_or_write()

        COMMAND_authentification2 = b"\x07\x02"
        KEY_VALIDATE_MODE = b"\x60"  # use KeyA
        BLOCK_ADDRESS = b"\x04"
        PASSWORD = b"\xff\xff\xff\xff\xff\xff"
        await self.send("authentification2", COMMAND_authentification2,
                        KEY_VALIDATE_MODE + BLOCK_ADDRESS + PASSWORD)

        COMMAND_read = b"\x08\x02"
        DATA = (await self.send("read", COMMAND_read, BLOCK_ADDRESS))[:-1]

        return DATA

    async def _write_to_tag(self, value_to_write: bytes) -> None:
        if len(value_to_write) != 16:  # validation
            raise ValueError("Value to write must be 16 bytes long")

        await self.select_card_for_read_or_write()

        COMMAND_authentification2 = b"\x07\x02"
        KEY_VALIDATE_MODE = b"\x60"  # use KeyA
        BLOCK_ADDRESS = b"\x04"
        PASSWORD = b"\xff\xff\xff\xff\xff\xff"
        await self.send("authentification2", COMMAND_authentification2,
                        KEY_VALIDATE_MODE + BLOCK_ADDRESS + PASSWORD)

        COMMAND_write = b"\x09\x02"
        await self.send("write", COMMAND_write, BLOCK_ADDRESS + value_to_write)

    async def wait_for_tag_read(self) -> bytes or None:
        """
        Waits for a tag to be read.
        Returns 16 bytes read from the tag.
        """

        await self.set_led_status(True)

        while self.can_write:
            try:
                return await self._read_from_tag()
            except ValueError as e:
                await asyncio.sleep(.1)
                continue

    async def write_to_tag_and_validate(self, value_to_write: bytes) -> bool:
        """
        Write to the tag and validate the write.
        Returns True if the write was successful, False otherwise.
        Doesn't allow to write the same value to the tag twice.
        """

        await self.set_led_status(True)

        for _ in range(10):
            if not self.can_write:
                await self.set_led_status(False)
                return False

            try:
                await self._write_to_tag(value_to_write)
                data = await self._read_from_tag()
                if data == value_to_write:
                    print("Write success:", data)
                    await self.set_led_status(False)
                    return True

            except ValueError as e:
                await asyncio.sleep(0.5)

        await self.set_led_status(False)
        return False


def debug_random_16_bytes() -> bytes:
    """
    generates random 16 bytes like these:
    b"\xaa\xaa\xaa\xba\xba\xba\xba\xba\xba\xba\xba\xba\xba\xba\xba\xee"
    """
    return bytes([random.randint(0, 255) for i in range(16)])


async def example_usage() -> None:
    """
    Example usage:
    connects tp the writer
    generates random 16 bytes to write to the tag
    writes to the tag, then reads from the tag to validate if it was
    successfully written.
    If everything is ok, the program will exit.
    """
    writer = Writer()

    while True:
        value_to_write = debug_random_16_bytes()
        print("value_to_write: ", value_to_write)
        while True:
            was_successful = await writer.write_to_tag_and_validate(value_to_write)
            if was_successful:
                break

    # # Other available commands:
    # print(writer.get_model_string())  # returns the model string
    # writer.blink_led(10)  # blinks the LED 10 times
    # writer.set_led_status(False)  # turn_off_led
    # writer.set_led_status(True)  # turn_on_led


if __name__ == "__main__":
    asyncio.run(example_usage())


# --- Not used, but might be useful ---

def print_device_info(dev) -> None:
    """
    Print information about the device.
    """
    print("Device: {0}".format(dev))
    print("ID: {0}".format(dev.idVendor))
    print("ID: {0}".format(dev.idProduct))
    print("Device Class: {0}".format(dev.bDeviceClass))
    print("Device SubClass: {0}".format(dev.bDeviceSubClass))
    print("Device Protocol: {0}".format(dev.bDeviceProtocol))
    print("Device Version: {0}".format(dev.bcdDevice))
    print("Manufacturer: {0}".format(dev.iManufacturer))
    print("Product: {0}".format(dev.iProduct))
    print("Serial: {0}".format(dev.iSerialNumber))


def print_device_info_short(dev) -> None:
    """
    Print short information about the connected device.
    """
    print("Manufacturer: %s" % dev.manufacturer)
    print("Product: %s" % dev.product)
    print("Serial No: %s" % dev.serial_number)
