#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import os
import csv
import sqlite3 as lite
import sys
import time
import datetime

#Directory list
def lister(root): 
	directory_list = ''
	for (thisdir, subshere, fileshere) in os.walk(root):
		directory_list = directory_list + thisdir
		i = 0
		for fname in fileshere:
			path = os.path.join(thisdir, fname)
			directory_list = directory_list + path
			i += 1
			
	return directory_list
		
my_list = ''
my_list = lister('../')

my_str = my_list.replace('../', '\n ')

con = lite.connect('../DB/mybase.db')
with con:
	cur = con.cursor()
	#cur.execute("UPDATE adminmanager_users SET bd_part_z='',bd_part_f='',flag_bd='False' WHERE login='gipnoz'")
	#cur.execute("DELETE FROM adminmanager_csvbox WHERE users_id=1")
	cur.execute("UPDATE adminmanager_directoryinfo SET directory_list='"+my_str+"' WHERE users_id=1")