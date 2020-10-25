#!/usr/bin/python3

import pymysql

pymysql.install_as_MySQLdb()

import MySQLdb

def open_connection():
	print('Opening connection ... ')
	conn = MySQLdb.connect(host='194.59.164.85', user='u430582279_adm', passwd='mypchub_2020p@$$w0rd', db='u430582279_pchub')
    return conn

def close_connection(conn):
    	print('CLosing connection ... ')
    if conn is not None:
        conn.close()
        conn = None    

def insert_transaction(account_id, card_id, latest_balance, loc_lat, loc_long):
	print('Insert Transaction ... ')
    conn = open_connection()
    close_connection(conn)


def test_connect():
    sqlquery = 'select * from transpo_rec'
    print('SQL QUERY' + sqlquery)
    print('Initiate Opening Connection ... ')
    conn = open_connection()
    cursor = conn.cursor()
    cursor.execute(sqlquery)
    row = cursor.fetchone()
    print('QUERY RESULT: '+ row)
    print('Initiate Closing Connection ... ')
    close_connection(conn)

if __name__ == "__main__":
    print('Database Service Main ... ')
    print('Testing connection ... ')
    test_connect()
