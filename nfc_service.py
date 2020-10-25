#!/usr/bin/python3

import board
import busio
import time
import struct

# Additional import needed for I2C/SPI
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B

from adafruit_pn532.spi import PN532_SPI

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

CARD_KEY = b'\xFF\xFF\xFF\xFF\xFF\xFF'
AMOUNT_BLOCK = 4

#10 seconds
timeout = 10


def init_service():
    #ic, ver, rev, support = pn532.get_firmware_version()
    #print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
    # Configure PN532 to communicate with MiFare cards
    pn532.SAM_configuration()


def authenticate_card():
    print('Waiting for RFID/NFC card!')

    timeout_start = time.time()

    while True:
        # Check if a card is available to read
        if time.time() > timeout_start + timeout:
            raise ValueError('Timeout')

        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is not None:
            break

    print('Found card with UID:', [hex(i) for i in uid])
    print("Authenticating block ...", AMOUNT_BLOCK)

    authenticated = pn532.mifare_classic_authenticate_block(
        uid, AMOUNT_BLOCK, MIFARE_CMD_AUTH_B, CARD_KEY)

    if authenticated:
        print('Authentication Success!')
        return True

    print("Authentication failed!")
    return False

def get_balance_from_card():
    print('Waiting for RFID/NFC card!')

    timeout_start = time.time()

    while True:
        # Check if a card is available to read
        if time.time() > timeout_start + timeout:
            raise ValueError('Timeout')

        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is not None:
            break

    print('Found card with UID:', [hex(i) for i in uid])
    print("Authenticating block ...", AMOUNT_BLOCK)

    authenticated = pn532.mifare_classic_authenticate_block(
        uid, AMOUNT_BLOCK, MIFARE_CMD_AUTH_B, CARD_KEY)

    if authenticated == False:
        raise ValueError('Card Authentication Failed')

    # Read block #4
    print('Wrote to Amount block , now trying to read that data:',
            [hex(x) for x in pn532.mifare_classic_read_block(AMOUNT_BLOCK)])

    dataread = pn532.mifare_classic_read_block(AMOUNT_BLOCK)

    #first 4 TEMP
    balance_byte_array = dataread[0:4]
    b = struct.unpack('f', balance_byte_array)
    balance = b[0]
    print('Balance is:', balance)
    return balance

def write_balance_to_card(balance):
    print('Waiting for RFID/NFC card!')

    timeout_start = time.time()

    while True:
        # Check if a card is available to read
        if time.time() > timeout_start + timeout:
            raise ValueError('Timeout')

        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is not None:
            break

    print('Found card with UID:', [hex(i) for i in uid])
    print("Authenticating block ...", AMOUNT_BLOCK)

    authenticated = pn532.mifare_classic_authenticate_block(
        uid, AMOUNT_BLOCK, MIFARE_CMD_AUTH_B, CARD_KEY)

    if authenticated == False:
        raise ValueError('Card Authentication Failed')

    data = bytearray(16)
    data[0:16] = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    balance_byte_array = struct.pack('f', balance)
    print(balance_byte_array)
    data[0:4] = balance_byte_array

    print(bytes(data).hex())

    # Write 16 byte block.
    pn532.mifare_classic_write_block(AMOUNT_BLOCK, data)

    # Read block #4
    print('Wrote to Amount block , now trying to read that data:',
            [hex(x) for x in pn532.mifare_classic_read_block(AMOUNT_BLOCK)])

    dataread = pn532.mifare_classic_read_block(AMOUNT_BLOCK)

    #first 4 TEMP
    balance_byte_array = dataread[0:4]
    b = struct.unpack('f', balance_byte_array)
    balance = b[0]
    print('New Balance is:', balance)
    return balance    

def get_balance():
    valid = authenticate_card()
    if valid:
        print('valid')
        balance = get_balance_from_card()
        return balance
    else:
        print('failed')
        raise ValueError('Card Authentication Failed')

def setup_card():
    print('Waiting for RFID/NFC card!')

    timeout_start = time.time()

    while True:
        # Check if a card is available to read
        if time.time() > timeout_start + timeout:
            raise ValueError('Timeout')

        uid = pn532.read_passive_target(timeout=0.5)
        # Try again if no card is available.
        if uid is not None:
            break

    print('Found card with UID:', [hex(i) for i in uid])
    print("Authenticating block ...", AMOUNT_BLOCK)

    authenticated = pn532.mifare_classic_authenticate_block(
        uid, AMOUNT_BLOCK, MIFARE_CMD_AUTH_B, CARD_KEY)

    if authenticated == False:
        raise ValueError('Card Authentication Failed')

    data = bytearray(16)
    data[0:16] = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    print(bytes(data).hex())

    # Write 16 byte block.
    pn532.mifare_classic_write_block(AMOUNT_BLOCK, data)

    # Read block #4
    print('Wrote to Amount block , now trying to read that data:',
            [hex(x) for x in pn532.mifare_classic_read_block(AMOUNT_BLOCK)])

    dataread = pn532.mifare_classic_read_block(AMOUNT_BLOCK)

    #first 4 TEMP
    balance_byte_array = dataread[0:4]
    b = struct.unpack('f', balance_byte_array)
    balance = b[0]
    print('Card Setup Done. New Balance is:', balance)
    return balance        

def reload(amount):
    valid = authenticate_card()
    if valid:
        print('valid')
        balance =  get_balance_from_card()
        balance = balance + amount
        balance = write_balance_to_card(balance)
        return balance
    else:
        print('failed')
        raise ValueError('Card Authentication Failed')


def pay(amount):
    valid = authenticate_card()
    if valid:
        print('valid')
        balance = get_balance_from_card()
        if balance < amount:
            raise ValueError('Insufficient Balance')
        balance = balance - amount
        balance = write_balance_to_card(balance)
        return balance
    else:
        print('failed')
        raise ValueError('Card Authentication Failed')


if __name__ == '__main__':
    print("Main Start - Test")
    try:
        init_service()
        valid = authenticate_card()
        print(valid)

    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print('Stopped')
