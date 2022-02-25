# Settings:
VERBOSE = False  # verbose prints about what is going on

# other constants, do not change
USB_INTERFACE_ID = 1

import random
import struct
import sys
from time import sleep, time
from sqlalchemy import true
import usb.core
import usb.util
import time

import usb.backend.libusb1
BACKEND = usb.backend.libusb1.get_backend(find_library=lambda x: "/usr/lib/libusb-1.0.so")

def pad_bytes_with_zeros(data, length):
        return data + (length - len(data)) * b"\x00"


def createSetReportBytes(command, data = b''):
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

    LEN = struct.pack("<H", len(device_id + command + data + CHECKSUM))  # 2 bytes, indicating the number of bytes from DeviceID to Checksum the left byte is used, and the right byte is also 0x00
    ALL = pad_bytes_with_zeros(preamble + LEN + device_id + command + data + CHECKSUM, 64)

    return ALL
    


class Writer:
    def __init__(self):
        print("Waiting for the writer to be connected")
        while True:
            # print("="*80)
            # print(usb.core.find(find_all=true, backend=BACKEND))
            # print("="*80)

            self.dev = usb.core.find(idVendor=0x0471, idProduct=0xa112)
            # self.dev = usb.core.find(idVendor=0x0444, idProduct=0xa112)
            if self.dev is None: 
                if VERBOSE:
                    print("Writer not found. Waiting for it to be connected")
                sleep(1)
            else:
                print("Successfully connected to the writer") 
                self.detach_kernel_driver(USB_INTERFACE_ID)
                break
                
        

    def detach_kernel_driver(self, usb_interface):
        """
        # fixes resource busy
        # https://stackoverflow.com/questions/67453535/i-keep-getting-usb-core-usberror-errno-16-resource-busy-when-trying-to-read
        """
        
        if self.dev.is_kernel_driver_active(USB_INTERFACE_ID):
            try:
                self.dev.detach_kernel_driver(USB_INTERFACE_ID)
                if VERBOSE:
                    print("Kernel driver detached to fix Resource busy error")
            except usb.core.USBError as e:
                sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(USB_INTERFACE_ID, str(e)))

    def set_report(self, description_type_and_index, usb_interface, data):
        """
        Send set_report to the writer.
        # 0x21 = REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_OUT
        """
        SET_REPORT = 0x09
        return self.dev.ctrl_transfer(0x21, SET_REPORT, description_type_and_index, usb_interface, data)

    def get_report(self, description_type_and_index, usb_interface, max_reply_size):
        """
        Recieve get_report from the writer.
        # 0xA1 = REQUEST_TYPE_CLASS | RECIPIENT_INTERFACE | ENDPOINT_IN
        """
        GET_REPORT = 0x01
        # max_reply_size = 64
        return self.dev.ctrl_transfer(0xa1, GET_REPORT, description_type_and_index, usb_interface, max_reply_size)

    def parse_set_report_response(self, request):
        """
        Parse set_report for debugging purposes.
        """
        request_bytes = bytes(request)
        LEN = struct.unpack("<H", request_bytes[2:4])[0]
        if VERBOSE:
            print("--- Request ---")
            print("Preamble: ", request_bytes[0:2])
            print("Length:   ", request_bytes[2:4])
            print("Device ID:", request_bytes[4:6])
            print("Command:  ", request_bytes[6:8])
            print("Data:     ", request_bytes[8:8 + LEN - 5])
            print("Checksum: ", request_bytes[-1])
            print("All:", request_bytes)
            print("")


    def parse_get_report_response(self, response):
        """
        Parse get_report for debugging purposes.
        Return the data part of the response.
        """
        response_bytes = bytes(response)

        LEN = struct.unpack("<H", response_bytes[2:4])[0]
        
        status = response_bytes[8:9]
        DATA = response_bytes[9:9 + LEN - 5]

        if VERBOSE:
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
            raise ValueError('Status is not 0x00, is tag placed on the writer? Please try again - sometimes it fails')

        return DATA


    # sends data and gets response
    def send(self, human_title, command, data = b''):
        """
        Wrapper to send data to the writer and get the response in a single function call
        """
        if len(command) != 2:  # validation
            raise ValueError("Command must be 2 bytes long")

        if VERBOSE:
            print("##########", human_title, "##########")
        set_report_bytes = createSetReportBytes(command, data)
        self.parse_set_report_response(set_report_bytes)
        response_len = self.set_report(0x301, 0x01, set_report_bytes)
        byte_array = self.get_report(0x301, 0x01, response_len)
        data = self.parse_get_report_response(byte_array)
        return data

    def turn_off_led(self):
        """
        Turn off the LED on the writer.
        """
        COMMAND_LED_CONTROL = b"\x07\x01"
        LED_OFF = b"\x00"
        self.send("Turning off LED", COMMAND_LED_CONTROL, LED_OFF)


    def turn_on_led(self):
        """
        Turn on the LED on the writer.
        """
        COMMAND_LED_CONTROL = b"\x07\x01"
        LED_ON = b"\x01"
        self.send("Turning on LED", COMMAND_LED_CONTROL, LED_ON)


    def blink_led(self, repeat = 1):
        """
        Blink the LED on the writer.
        repeat: number of times to blink
        """
        for i in range(repeat):
            self.turn_off_led()
            sleep(.1)
            self.turn_on_led()
            sleep(.1)

    
    def get_model_string(self):
        """
        Get the connected model string from the writer.
        """
        COMMAND_GET_MODEL_STRING = b"\x04\x01"
        return self.send("Getting model string", COMMAND_GET_MODEL_STRING)

    def select_card_for_read_or_write(self):
        """
        Select the card nearby for read or write.
        Success if self.send() at all steps won't raise an error.
        """
        COMMAND = b"\x0c\x01"
        DATA = b"\x00"  # turn off RF
        self.send("antena_sta", COMMAND, DATA)

        COMMAND = b"\x08\x01"
        DATA = b"\x41"
        self.send("init_type", COMMAND, DATA)

        COMMAND = b"\x0c\x01"
        DATA = b"\x01"  # turn on RF
        self.send("antena_sta", COMMAND, DATA)

        COMMAND = b"\x01\x02"
        DATA = b"\x52"
        self.send("request", COMMAND, DATA)

        COMMAND = b"\x02\x02"
        DATA = b"\x04"
        CARD_SERIAL = self.send("anticol", COMMAND, DATA)[:-1]

        COMMAND = b"\x03\x02"
        self.send("select", COMMAND, CARD_SERIAL)
            
    def read_from_tag(self):
        """
        Read the tag.
        WARNING: sometimes the tag is not read correcty. Use self.read_tag_with_retry() to repeat read operation until success.
        """

        self.select_card_for_read_or_write()

        COMMAND = b"\x07\x02"
        KEY_VALIDATE_MODE = b"\x60"  # use KeyA
        BLOCK_ADDRESS = b"\x04"
        PASSWORD = b"\xff\xff\xff\xff\xff\xff"
        self.send("authentification2", COMMAND, KEY_VALIDATE_MODE + BLOCK_ADDRESS + PASSWORD)

        COMMAND = b"\x08\x02"
        DATA = self.send("read", COMMAND, BLOCK_ADDRESS)[:-1]
        
        return DATA

    def write_to_tag(self, value_to_write):
        if len(value_to_write) != 16:  # validation
            raise ValueError("Value to write must be 16 bytes long")

        self.select_card_for_read_or_write()

        COMMAND = b"\x07\x02"
        KEY_VALIDATE_MODE = b"\x60"  # use KeyA
        BLOCK_ADDRESS = b"\x04"
        PASSWORD = b"\xff\xff\xff\xff\xff\xff"
        self.send("authentification2", COMMAND, KEY_VALIDATE_MODE + BLOCK_ADDRESS + PASSWORD)

        COMMAND = b"\x09\x02"
        DATA = self.send("write", COMMAND, BLOCK_ADDRESS + value_to_write)[:-1]

    def wait_for_tag_read(self):
        """
        Waits for a tag to be read.
        Returns 16 bytes read from the tag.
        """
        while True:
            try:
                time.sleep(0.1)
                return self.read_from_tag()
                break
            except:
                if VERBOSE:
                    print("No tag nearby")

    def wait_for_tag_write(self, value_to_write):
        """
        Waits for a tag to be written to.
        Returns after successfully writen to the tag
        Will not read the tag if the data is really written to the tag, we use status code returned from the writer (status code 0x00 means success)
        """

        while True:
            try:
                time.sleep(0.1)
                self.write_to_tag(value_to_write)
                break
            except Exception as e:
                if VERBOSE:
                    print("No tag nearby")
                    print(e)

    def write_to_tag_and_validate(self, value_to_write):
        """
        Write to the tag and validate the write.
        """

        # print("Ready to write", value_to_write)
        self.wait_for_tag_write(value_to_write)
        DATA = self.wait_for_tag_read()
        if DATA == value_to_write:
            # print("Data successfully written")
            self.blink_led(5)
            time.sleep(3)
            # return "Data successfully written"
            return



def debug_random_16_bytes():
    """
    generates random 16 bytes like these:
    b"\xaa\xaa\xaa\xba\xba\xba\xba\xba\xba\xba\xba\xba\xba\xba\xba\xee"
    """
    return bytes([random.randint(0, 255) for i in range(16)])



if __name__ == "__main__":
    """
    Example usage:
    connects tp the writer
    generates random 16 bytes to write to the tag
    writes to the tag, then reads from the tag to validate if it was successfully written.
    If everything is ok, the program will exit.
    """
    writer = Writer()

    value_to_write = debug_random_16_bytes()
    writer.write_to_tag_and_validate(value_to_write)

    # Other available commands:
    # print(writer.get_model_string())  # returns the model string
    # writer.blink_led(10)  # blinks the LED 10 times
    # writer.turn_on_led()  
    # writer.turn_off_led()










# --- Not used, but might be useful ---

def print_device_info(dev):
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

def print_device_info_short(dev):
    """
    Print short information about the connected device.
    """
    print("Manufacturer: %s" % dev.manufacturer)
    print("Product: %s" % dev.product)
    print("Serial No: %s" % dev.serial_number)


