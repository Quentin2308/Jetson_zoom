# zoom normal vers l'avant : sudo python3 test.py -z zoomin
# zoom normal vers l'arrière : sudo python3 test.py -z zoomout
# zoom vers l'avant à vitesse variable allant de 0 à 7 (ici 2) : sudo python3 test.py -z zoomin -s 2
# zoom vers l'arrière à vitesse variable allant de 0 à 7 (ici 2) : sudo python3 test.py -z zoomout -s 2
# arrêt du zoom : sudo python3 test.py ou CTRL+C pendant l'exécution du code
# digital zoom par défaut en x1 sinon configurable de 0 à 5 (x1 à x12) : sudo python3 test.py -z zoomin -s 2 -d 3

import time
import serial
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-z", "--zoom", type=str,
    help="zoom position")
ap.add_argument("-s", "--speed", type=int,
    help="zoom speed between 0 and 7")
ap.add_argument("-d", "--digitalzoom", type=int,
    help="digital zoom mode between 0 and 5")
args = vars(ap.parse_args())

print("UART Program")
print("NVIDIA Jetson Nano Developer Kit")

def byteSet(by, value, position):
	by[position] = value
	return by

zoom_out_max = [b'\x90', b'P', b'\x00', b'\x00', b'\x00', b'\x00', b'\xff']
zoom_in_D5_max = [b'\x90', b'P', b'\x08', b'\x0c', b'\x04', b'\x00', b'\xff']
#zoom_in_D4_max = [b'\x90', b'P', b'\x04', b'\x00', b'\x00', b'\x00', b'\xff']
#zoom_in_D3_max = [b'\x90', b'P', b'\x04', b'\x00', b'\x00', b'\x00', b'\xff']
#zoom_in_D2_max = [b'\x90', b'P', b'\x04', b'\x00', b'\x00', b'\x00', b'\xff']
#zoom_in_D1_max = [b'\x90', b'P', b'\x04', b'\x00', b'\x00', b'\x00', b'\xff']
zoom_in_D0_max = [b'\x90', b'P', b'\x04', b'\x00', b'\x00', b'\x00', b'\xff']

class Commands:
    adress_set = bytearray.fromhex("883001FF")
    PowerOn = bytearray.fromhex("8101040002FF")
    PowerOff = bytearray.fromhex("8101040003FF")
    Cam_DZoom_0 = bytearray.fromhex("8101042600ff")
    Cam_DZoom_1 = bytearray.fromhex("8101042601ff")
    Cam_DZoom_2 = bytearray.fromhex("8101042602ff")
    Cam_DZoom_3 = bytearray.fromhex("8101042603ff")
    Cam_DZoom_4 = bytearray.fromhex("8101042604ff")
    Cam_DZoom_5 = bytearray.fromhex("8101042605ff")
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

    if not args.get("digitalzoom",False):
	serial_port.write(Commands.Cam_DZoom_0)	

    elif args["digitalzoom"] == 0 :
	serial_port.write(Commands.Cam_DZoom_0)	
	
    elif args["digitalzoom"] == 1 :
	serial_port.write(Commands.Cam_DZoom_1)
	
    elif args["digitalzoom"] == 2 :
	serial_port.write(Commands.Cam_DZoom_2)
	
    elif args["digitalzoom"] == 3 :
	serial_port.write(Commands.Cam_DZoom_3)
	
    elif args["digitalzoom"] == 4 :
	serial_port.write(Commands.Cam_DZoom_4)
	
    elif args["digitalzoom"] == 5 :
	serial_port.write(Commands.Cam_DZoom_5)

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
	
    zoom_max = False
    while not zoom_max : 	
        serial_port.write(Inquiry.ZoomPos)
        packet = []
        finished_packet = False
        while not finished_packet :
            if serial_port.inWaiting() > 0:
		
            	s=serial_port.read()
            	#print("s = ", s)
		
            	if s == b'\xff' :
            	    
            	    packet.append(s)
            	    print(packet)
            	    
            	    if args["zoom"] == "zoomin":
			if packet == zoom_in_D0_max and not args.get("digitalzoom", False):
            	            serial_port.write(Commands.ZoomStop)
            	            zoom_max = True
			elif packet == zoom_in_D0_max and args["digitalzoom"] == 0 :
            	            serial_port.write(Commands.ZoomStop)
            	            zoom_max = True
			#elif packet == zoom_in_D1_max and args["digitalzoom"] == 1 :
            	            #serial_port.write(Commands.ZoomStop)
            	            #zoom_max = True
			#elif packet == zoom_in_D2_max and args["digitalzoom"] == 2 :
            	            #serial_port.write(Commands.ZoomStop)
            	            #zoom_max = True
			#elif packet == zoom_in_D3_max and args["digitalzoom"] == 3 :
            	            #serial_port.write(Commands.ZoomStop)
            	            #zoom_max = True
			#elif packet == zoom_in_D4_max and args["digitalzoom"] == 4 :
            	            #serial_port.write(Commands.ZoomStop)
            	            #zoom_max = True
			elif packet == zoom_in_D5_max and args["digitalzoom"] == 5 :
            	            serial_port.write(Commands.ZoomStop)
            	            zoom_max = True
			
            	    elif packet == zoom_out_max and args["zoom"] == "zoomout":
            	        serial_port.write(Commands.ZoomStop)
            	        zoom_max = True
			
            	    finished_packet = True
            	
            	else :
		    
            	    packet.append(s)
            	
            	if s == "\r".encode():
                # For Windows boxen on the other end
            	    serial_port.write("\n".encode())

except KeyboardInterrupt:
    serial_port.write(Commands.ZoomStop)
    print("Exiting Program")

#except Exception as exception_error:
    #print("Error occurred. Exiting Program")
    #print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass
