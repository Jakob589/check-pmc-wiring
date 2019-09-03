import csv
import time
import socket
import subprocess 
import zerorpc
import sys
import os
 
def save_ip_txt(ip):
	f= open("pmc_ip.csv","w+")
	f.write(ip)


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
		cntr += 3
		if cntr > 1:
			print("Device not found, please try again. Check if PMC is connected to power.",end='')
			exit()
		
		
			
#first start avahi-daemon with "service_name"
service_name = "saam-pmc"
ip = get_service(service_name)


c = zerorpc.Client()
c.connect("tcp://%s" % ip)

if True:
	try:
		msg = c.test("response: %s" % service_name)
		print(msg,end='')
	except:
		print("Device not found, please try again. Check if PMC is connected to power.",end='')
		
sys.stdout.flush()

