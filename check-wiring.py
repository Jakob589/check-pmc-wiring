#!/usr/bin/env python3

import time
import csv
import socket
import subprocess 
import zerorpc
import sys
import os
 
def get_service(service_name):
	cntr = 1
	while True:
		avahi = subprocess.check_output(["avahi-browse","-rptk","_remote._tcp"])
		avahi = csv.reader(avahi.decode().split('\n'), delimiter=';')
		for row in avahi:
			if row and row[0] == "=" and service_name in row:
				try:
					socket.inet_aton(row[7])
					srv = row[7] + ":" + row[8]
					#print("Service " + service_name + " discovered: " + srv)
					return srv
				except socket.error:
					pass
		time.sleep(5)
		cntr += 1
		if cntr > 3:
			print("Device not found, please try again. Check if PMC is connected to power.",end='')
			exit()
		
		
			
#first start avahi-daemon with "service_name"
service_name = "saam-pmc"
ip = get_service(service_name)

loc_id = open('/etc/lgtc/loc-id').readline().strip()

c = zerorpc.Client()
c.connect("tcp://%s" % ip)

if True:
	try:
		msg = c.test(loc_id) ##send location id
		print(msg,end='')
	except:
		print("Device not found, please try again. Check if PMC is connected to power.",end='')
		
sys.stdout.flush()

