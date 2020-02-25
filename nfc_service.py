#!/usr/bin/python3

import board
import busio

# Additional import needed for I2C/SPI
from digitalio import DigitalInOut
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B

from adafruit_pn532.spi import PN532_SPI

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

key = b'\xFF\xFF\xFF\xFF\xFF\xFF'


def init_service():
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
    # Configure PN532 to communicate with MiFare cards
    pn532.SAM_configuration()


def authenticate_card():
    print('Waiting for RFID/NFC card!')

    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        #print('.', end="")
        # Try again if no card is available.
        if uid is not None:
            break

    print('Found card with UID:', [hex(i) for i in uid])
    print("Authenticating block 4 ...")

    authenticated = pn532.mifare_classic_authenticate_block(
        uid, 4, MIFARE_CMD_AUTH_B, key)

    if authenticated:
        print('Authentication Success!')
        return True

    print("Authentication failed!")
    return False


def get_balance():
    valid = authenticate_card()
    if valid:
        print('valid')
        balance = 100
        return balance
    else:
        print('failed')
        raise ValueError('Card Authentication Failed')


def reload(amount):
    valid = authenticate_card()
    if valid:
        print('valid')
        balance = 100
        balance = balance + amount
        return balance
    else:
        print('failed')
        raise ValueError('Card Authentication Failed')


def pay(amount):
    valid = authenticate_card()
    if valid:
        print('valid')
        balance = 100
        balance = balance - amount
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
