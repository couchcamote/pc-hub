#!/usr/bin/python3

import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

if __name__ == "__main__":
    print('Config Main ... ')

    print(parser.get('app', 'start_message'))

