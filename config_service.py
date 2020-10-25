#!/usr/bin/python3

import configparser

parser = configparser.ConfigParser()
parser.read('config.ini')

def get_value(section, config)
    return parser.get(section, config)

if __name__ == "__main__":
    print('Config Main ... ')

    print(get_value('app', 'start_message'))

