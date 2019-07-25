import csv
import time
import socket
import subprocess
import zerorpc

def save_ip_txt(ip):
	f= open("pmc_ip.csv","w+")
	f.write(ip)



def get_service(service_name):
	while True:
		avahi = subprocess.check_output(["avahi-browse","-rptk","_remote._tcp"])
		avahi = csv.reader(avahi.decode().split('\n'), delimiter=';')
		for row in avahi:
			if row and row[0] == "=" and service_name in row:
				try:
					socket.inet_aton(row[7])
					srv = row[7] + ":" + row[8]
					print("Service " + service_name + " discovered: " + srv)
					return srv
				except socket.error:
					pass

		time.sleep(10)
#first start avahi-daemon with "service_name"
service_name = "saam-pmc"
ip = get_service(service_name)


c = zerorpc.Client()
c.connect("tcp://%s" % ip)
msg = c.test("testing: %s" % service_name)
print(msg)
