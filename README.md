# check-pmc-wiring
pmc-check-wiring.py is running on PMC, it is automatically run by systemd service. check-wiring.py is run manually on eGW when we want to check if pmc is wired correctly

INITIALIZE:

ON eGATEWAY:
1. Start avahi-daemon, it will enable devices to find themselves in a big network.
2. Run "check-wiring.py"  
3. Check output 

ON PMC: (serial port on pmc is "ttyS2") 

1. Start avahi-daemon with XML script - use unique service names like saam-pmc1,2,3,...!
2. Run "$ bash wams-test.sh" to see if serial is working
3. run pmc-check-wiring.py if not already ****AT THIS POINT I COULD NOT IMPLEMENT EXTRA SPECEFICATIONS, SINCE I DO NOT HAVE THEM YET****

Troubleshooting:
if serial is not working: 
- Run "$ bash set.gpio 59 1" (script location is on sensorlab github cb-iot repository)
- Also if you had to run this command manualy create a new service in systemd that
will automaticly run and remap serial ports.
- Make sure that your script has suitable shebang (#!/usr/bin/env python3)

If no response:
- Run systemctl start pmc-check-wiring.service 
- If not created already create service that will run this service automaticly

For other problems contact me:
jakob.jenko@gmail.com
