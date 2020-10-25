#!/usr/bin/python3

import configparser

parser = configparser.ConfigParser()
parser.read('config.ini')

if __name__ == "__main__":
    print('Config Main ... ')

    print(parser.get('app', 'start_message'))

