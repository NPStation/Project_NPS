#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import os
import csv
import sqlite3 as lite
import sys
import time
import datetime
import collections

#Directory list

def lister(root):
	directory_list = {}
	counter = [0]*999
	path_list = ['']*999
	for (thisdir, subshere, fileshere) in os.walk(root):
		i = 0
		#directory_list = directory_list + thisdir
		for fname in fileshere:
			path = os.path.join(thisdir, fname)
			path_list[i] = path
			counter[i] = i
			i += 1
	
	directory_list = dict(zip(counter, path_list))
	return directory_list
	

my_list = {}
my_list = lister('../')

#my_str = my_list.replace('../', '\n ')

list_size = len(my_list)
for j in range(list_size):
	print my_list.values()[j], my_list.keys()[j]
	
#my_str = my_list.replace('../', '\n ')

con = lite.connect('../DB/npbase.db')
with con:
	cur = con.cursor()
	for j in range(list_size):
		cur.execute("INSERT INTO np_server_device VALUES("+str(my_list.keys()[j])+",'"+my_list.values()[j]+"','"+str(my_list.keys()[j])+"', 1)")

		
		
		
python manage.py sqlall np_server
python manage.py syncdb
python manage.py runserver 0.0.0.0:8000
#Добавление устройства
from np_server.models import *	
in_device = Device.objects.create(user_id='1', model='Gsmart 1345', imei='3567658767',phone_number='79817102218', mac='', usbidcode='',latitude='59.96101',longitude='30.29227',height='7.6',cell_id=False,ip_info='',wifi_info='', battery_info='60%', webcam_picture='')
in_device.save()

save_status = ClientStatus.objects.create(user_id='1',model='Gsmart 1345',alarm='False',warning='False',blocking='False',privacy='False',search_status='False',monitor_status='False')
save_status.save()


cell_save = CellId.objects.create(user_id='1',model='Gsmart 1345',mcc='250',mnc='01',lac='30445',cid='88080833')
cell_save.save()








