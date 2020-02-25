#!/usr/bin/python3

from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *

import binascii
import socket
import time
import signal
import sys

# Configure the key to use for writing to the MiFare card.  You probably don't
# need to change this from the default below unless you know your card has a
# different key associated with it.
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

# Number of seconds to delay after reading data.
DELAY = 0.5

# Prefix, aka header from the card
HEADER = b'BG'

signal.signal(signal.SIGINT, close)

pn532 = Pn532_i2c()
pn532.SAMconfigure()

def close(signal, frame):
        sys.exit(0)

print('PN532 NFC RFID 13.56MHz Card Reader')
while True:
    # Wait for a card to be available
    uid = pn532.read_passive_target()
    # Try again if no card found
    if uid is None:
        continue
    # Found a card, now try to read block 4 to detect the block type
    print('')
    print('Card UID 0x{0}'.format(binascii.hexlify(uid)))
    # Authenticate and read block 4
    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                   CARD_KEY):
        print('Failed to authenticate with card!')
        continue
    data = pn532.mifare_classic_read_block(4)
    if data is None:
        print('Failed to read data from card!')
        continue
    # Check the header
    if data[0:2] !=  HEADER:
        print('Card is not written with proper block data!')
        continue
    # Parse out the block type and subtype
    print('User Id: {0}'.format(int(data[2:8].decode("utf-8"), 16)))
    time.sleep(DELAY);
