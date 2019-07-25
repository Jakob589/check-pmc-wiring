import zerorpc
import serial
import io

def serial_read(field_number):
    ser = serial.Serial('/dev/ttyS2',
                        baudrate=115200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_ODD,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1)

    sio = io.TextIOWrapper(io.BufferedReader(ser))

    serial_data = sio.readline()
    data = serial_data.strip().split(',')
    
    
    return float(data[field_number])
    
#check documentation for locations of other measurements
cosFi1 = serial_read(26)
cosFi2 = serial_read(27)
cosFi3 = serial_read(28)


class testPMC_RPC(object):
    def test(self, name): 

       

        #with if functions check if wired correctly          
        if cosFi1 > -0.2 and cosFi1 < 1:
            return "%s is wired correctly." % name
        else:
            return "%s wiring is faulty." % name

s = zerorpc.Server(testPMC_RPC())
s.bind("tcp://0.0.0.0:4242")
s.run()
