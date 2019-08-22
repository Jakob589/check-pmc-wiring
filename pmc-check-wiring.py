import zerorpc
import serial
import io


def serial_read():
    ser = serial.Serial('/dev/ttyS2',
                        baudrate=115200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_ODD,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1)

    sio = io.TextIOWrapper(io.BufferedReader(ser))

    serial_data = sio.readline()
    data = serial_data.strip().split(',')
    
    return data
    


class testPMC_RPC(object):
    def test(self, name): 

        data = serial_read()
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
        phase2ActivePower = float(data[18])
        phase3ActivePower = float(data[19])
        cosFi1 = float(data[26])
        cosFi2 = float(data[27])
        cosFi3 = float(data[28])

        
        if phase2AngleV < 100 or phase3AngleV > -100: #phase angle 2 is around 120deg and phase angle 3 around -120deg      
        # one phase:
        
            if  phase1CurrentRMS < 0.1:
                return "%s has faulty wiring. FIX: Check if current trasnformer is connected, or turn on load that draws more than 0.1A. \n I = %.2f." % (name , phase1CurrentRMS)
            
            elif phase1ActivePower < 0 or cosFi1 < -0.1:
                return "%s has faulty wiring. FIX: Check current trasnformer or voltage line polarity. \n W = %.2f \n cosFi = %.2f" % (name, phase1ActivePower, cosFi1)
            
            elif phase1VoltageRMS < 200 or phase1VoltageRMS > 250:
                return "%s has faulty wiring. FIX: Check voltage wires if connected to L1. \n U = %.2f \n " % (name, phase1VoltageRMS, freq)
            
            else: #return data for debuging
                return "%s is wired correctly. \n Voltage: %.2f V \n Current: %.2f A \n Active power: %.2f W  \n Freqency: %.2f Hz \n CosFi: %.2f \n Angle: 1= %.2f* 2=%.2f* \n   " % (name, phase1VoltageRMS, phase1CurrentRMS, phase1ActivePower, freq, cosFi1, phase2AngleV, phase3AngleV)
        
        
        
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
                return "%s has faulty wiring on phase 1. FIX: Check that the voltage measurement channel, CT channel and load are on the same phase. \n COS(phi) = %.2f " % (name, cosFi1)
           
            elif cosFi2 < 4 or cosFi2 > 100:
                return "%s has faulty wiring on phase 2. FIX: Check that the voltage measurement channel, CT channel and load are on the same phase. \n COS(phi) = %.2f " % (name, cosFi2)
            
            elif cosFi3 < 4 or cosFi3 > 100:
                return "%s has faulty wiring on phase 3. FIX: Check that the voltage measurement channel, CT channel and load are on the same phase. \n COS(phi) = %.2f " % (name, cosFi2)
            
            elif phase2AngleV < 100 or phase2AngleV > 150:
                return "%s has faulty wiring, phase 1 and 2 are the same. FIX: connect L2 to different phase than L1 or L3 \n angle 2 = %.2f° " % (name, phase2AngleV) 
            
            elif phase3AngleV > -100 or phase3AngleV < -150 :
                return "%s has faulty wiring, phase 2 and 3 are the same. FIX: connect L3 to different phase than L2 or L1 \n angle 3 = %.2f° " % (name, phase3AngleV) 

            else: #return data for debuging
                return "%s is wired correctly.\n Voltage: 1= %.2f 2= %.2f 3= %.2f \n Current: 1= %.2f 2= %.2f 3= %.2f \n Active power: 1= %.2f 2= %.2f 3= %.2f \n Cos(phi): 1= %.2f 2= %.2f 3= %.2f \n freq = %.2f \n theta2 = %.2f  theta3 = %.2f " % (name, phase1VoltageRMS, phase2VoltageRMS, phase3VoltageRMS, phase1CurrentRMS, phase2CurrentRMS, phase3CurrentRMS,phase1ActivePower,phase2ActivePower,phase3ActivePower, cosFi1, cosFi2, cosFi3, freq, phase2AngleV, phase3AngleV)


s = zerorpc.Server(testPMC_RPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
