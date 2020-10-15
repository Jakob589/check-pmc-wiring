#!/usr/bin/env python3

import zerorpc
import serial
import os
import time

def serial_read():
    
    ser = serial.Serial('/dev/ttyS2',
                        baudrate=115200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_ODD,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1)
    
    for x in range(5):
        try:

            serial_data = ser.readline().decode('utf-8').split(",")

            if len(serial_data) != 54:
                raise ValueError("len err") 
            
            print("returned data")
            ser.reset_output_buffer()
            ser.reset_input_buffer()
            ser.close() 
            return serial_data

        except:
            print("serial error")
            time.sleep(.5)
            continue

    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.close() 
    print("exited with null")



class testPMC_RPC(object):
    def test(self, name): 

        f = open("/root/SAAM_NILM/loc-id", "w+")
        f.write(name + "\n") # write loc id to alogorithm folder
        f.close

        os.system('systemctl stop saam-comread.service')
        os.system('sleep 50000 && systemctl start saam-comread.service &')

        data = serial_read()

        os.system('timeout 1 sudo getty -L -f 115200 ttyS2 vt100')
        os.system('systemctl start saam-comread.service')	 

        if data == None:
            return"%s has problem with serial port, please try again. If this keeps happening reboot PMC" % (name)

        phase1VoltageRMS = float(data[1])
        phase2VoltageRMS = float(data[2])
        phase3VoltageRMS = float(data[3])
        phase1CurrentRMS = float(data[4]) 
        phase2CurrentRMS = float(data[5]) 
        phase3CurrentRMS = float(data[6]) 
        freq = float(data[8])
        phase2AngleV = float(data[9]) # angle between first and second phase - normally around 120°
        phase3AngleV = float(data[10]) # angle between third and second phase - normally around -120°     
        phase1ActivePower = float(data[17])
        #phase2ActivePower = float(data[18])
        #phase3ActivePower = float(data[19])
        cosFi1 = float(data[26])
        cosFi2 = float(data[27])
        cosFi3 = float(data[28])

        
        if phase2AngleV < 100 or phase3AngleV > -100: #phase angle 2 is around 120deg and phase angle 3 around -120deg      
        # one phase:
        
            if  phase1CurrentRMS < 0.1:
                return "%s has faulty wiring. FIX: Check if current trasnformer is connected, or turn on load that draws more than 0.1A.  I = %.2f." % (name , phase1CurrentRMS)
            
            elif phase1ActivePower < 0 or cosFi1 < -0.1:
                return "%s has faulty wiring. FIX: Check current trasnformer or voltage line polarity. W = %.2f  cosFi = %.2f" % (name, phase1ActivePower, cosFi1)
            
            elif phase1VoltageRMS < 200 or phase1VoltageRMS > 250:
                return "%s has faulty wiring. FIX: Check voltage wires if connected to L1.  U = %.2f " % (name, phase1VoltageRMS)
            
            else: 
                return "OK"
        
        
        
        else: 
        # three phase:

            if  phase1CurrentRMS < 0.1:
                return "%s has faulty wiring. FIX: Check if phase 1 current trasnformer is connected, or turn on bigger load. I1 = %.2f " % (name, phase1CurrentRMS)
            
            elif  phase2CurrentRMS < 0.1:
                return "%s has faulty wiring. FIX: Check if phase 2 current trasnformer is connected, or turn on bigger load. I2 = %.2f " % (name, phase2CurrentRMS)
            
            elif  phase3CurrentRMS < 0.1:
                return "%s has faulty wiring. FIX: Check if phase 3 current trasnformer is connected, or turn on bigger load. I3 = %.2f " % (name, phase3CurrentRMS)
              
            elif phase1VoltageRMS < 200 or phase1VoltageRMS > 250:
                return "%s has faulty wiring. FIX: Check phase 1 voltage wires. U1 = %.2f " % (name, phase1VoltageRMS)
            
            elif phase2VoltageRMS < 200 or phase2VoltageRMS > 250:
                return "%s has faulty wiring. FIX: Check phase 2 voltage wires. U2 = %.2f" % (name, phase2VoltageRMS) 
            
            elif phase3VoltageRMS < 200 or phase3VoltageRMS > 250:
                return "%s has faulty wiring. FIX: Check phase 3 voltage wires. U3 = %.2f" % (name, phase3VoltageRMS)
            
            elif cosFi1 < 4 or cosFi1 > 100:
                return "%s has faulty wiring on phase 1. FIX: Check that the voltage measurement channel, CT channel and load are on the same phase. COS(phi) = %.2f " % (name, cosFi1)
           
            elif cosFi2 < 4 or cosFi2 > 100:
                return "%s has faulty wiring on phase 2. FIX: Check that the voltage measurement channel, CT channel and load are on the same phase. COS(phi) = %.2f " % (name, cosFi2)
            
            elif cosFi3 < 4 or cosFi3 > 100:
                return "%s has faulty wiring on phase 3. FIX: Check that the voltage measurement channel, CT channel and load are on the same phase. COS(phi) = %.2f " % (name, cosFi2)
            
            elif phase2AngleV < 100 or phase2AngleV > 150:
                return "%s has faulty wiring, phase 1 and 2 are the same. FIX: connect L2 to different phase than L1 or L3  angle 2 = %.2f° " % (name, phase2AngleV) 
            
            elif phase3AngleV > -100 or phase3AngleV < -150 :
                return "%s has faulty wiring, phase 2 and 3 are the same. FIX: connect L3 to different phase than L2 or L1  angle 3 = %.2f° " % (name, phase3AngleV) 

            else: #return data for debuging
                return "OK"


s = zerorpc.Server(testPMC_RPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
