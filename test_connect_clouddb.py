#!/usr/bin/python3

import pymysql

pymysql.install_as_MySQLdb()

import MySQLdb

conn = MySQLdb.connect(host='localhost', user='dbuser', passwd='dbpassword', db='db')
cursor = conn.cursor()

sqlquery = 'select * from transpo_rec'

print(sqlquery)

cursor.execute(sqlquery)
row = cursor.fetchone()

conn.close()

print(row)
