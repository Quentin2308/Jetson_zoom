# zoom normal vers l'avant : sudo python3 test.py -z zoomin
# zoom normal vers l'arrière : sudo python3 test.py -z zoomout
# zoom vers l'avant à vitesse variable allant de 0 à 7 (ici 2) : sudo python3 test.py -z zoomin -s 2
# zoom vers l'arrière à vitesse variable allant de 0 à 7 (ici 2) : sudo python3 test.py -z zoomout -s 2
# arrêt du zoom : sudo python3 test.py ou CTRL+C pendant l'exécution du code

import time
import serial
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-z", "--zoom", type=str,
    help="zoom position")
ap.add_argument("-s", "--speed", type=int,
    help="zoom speed between 0 and 7")
args = vars(ap.parse_args())

print("UART Program")
print("NVIDIA Jetson Nano Developer Kit")

def byteSet(by, value, position):
	by[position] = value
	return by

class Commands:
    adress_set = bytearray.fromhex("883001FF")
    PowerOn = bytearray.fromhex("8101040002FF")
    PowerOff = bytearray.fromhex("8101040003FF")
    ZoomStop = bytearray.fromhex("8101040700FF")
    ZoomTele = bytearray.fromhex("8101040702FF")
    ZoomWide = bytearray.fromhex("8101040703FF")
    def ZoomTeleVariable(self, speed):
        return byteSet(self.ZoomTele, (speed & 7) | 0x20, 4)
    def ZoomWideVariable(self, speed):
        return byteSet(self.ZoomTele, (speed & 7) | 0x30, 4)
Commands = Commands()

class Inquiry:
	Power = bytearray.fromhex("81090400ff")
	ZoomPos = bytearray.fromhex("81090447ff")

serial_port = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
# Wait a second to let the port initialize
time.sleep(1)
 
try:
    serial_port.write(Commands.adress_set)
    if args["zoom"] == "zoomin" :
        if not args.get("speed", False):
            serial_port.write(Commands.ZoomTele)
        else :
            speed = args["speed"]
            serial_port.write(Commands.ZoomTeleVariable(speed))
            
    elif args["zoom"] == "zoomout" :
        if not args.get("speed", False):
            serial_port.write(Commands.ZoomWide)
        else : 
            speed = args["speed"]
            serial_port.write(Commands.ZoomWideVariable(speed))
    
    else :
        serial_port.write(Commands.ZoomStop)
    
    while True: 
		
#ajout
        if serial_port.inWaiting() > 0:
            packet=''
            count=0
            while count<16:
            	s=serial_port.read(1)
            	if s:
            	    byte = ord(s)
            	    count+=1
            	    packet=packet+chr(byte)
           	else:
            	    print ("ERROR: Timeout waiting for reply")
            	    break
            	if byte==0xff:
            	    break
            print (packet)
            if data == "\r".encode():
                # For Windows boxen on the other end
                serial_port.write("\n".encode()
#fin de l'ajout			

        #if serial_port.inWaiting() > 0:
            #data = serial_port.read()
            #print(data)
            # if we get a carriage return, add a line feed too
            # \r is a carriage return; \n is a line feed
            # This is to help the tty program on the other end 
            # Windows is \r\n for carriage return, line feed
            # Macintosh and Linux use \nrt.w
            #if data == "\r".encode():
                # For Windows boxen on the other end
                #serial_port.write("\n".encode())
    

except KeyboardInterrupt:
    serial_port.write(Commands.ZoomStop)
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass
