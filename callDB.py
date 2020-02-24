#!/usr/bin/python

import MySQLdb

conn = MySQLdb.connect(host='194.59.164.85', user='u430582279_adm', passwd='pchubadm2020', db='u430582279_pchub')
cursor = conn.cursor()

sqlquery = 'select * from transpo_rec'

print(sqlquery)

cursor.execute(sqlquery)
row = cursor.fetchone()

conn.close()

print(row)
