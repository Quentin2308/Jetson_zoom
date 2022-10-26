
import time
import serial
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--power", type=str,
    help="camera power")
args = vars(ap.parse_args())

print("UART Program")
print("NVIDIA Jetson Nano Developer Kit")

power_on = 
power_off =

class Commands:
  adress_set = bytearray.fromhex("883001FF")
  PowerOn = bytearray.fromhex("8101040002FF")
  PowerOff = bytearray.fromhex("8101040003FF")
Commands = Commands()

class Inquiry:
  Power = bytearray.fromhex("81090400ff")
    
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
    serial_port.write(Commands.PowerOn)	
         
  power = False
  while not power :
    serial_port.write(Inquiry.Power)
    packet = []
    finished_packet = False
    
    while not finished_packet :
      
      if serial_port.inWaiting() > 0:
        s=serial_port.read()
        
        if s == b'\xff' :
          packet.append(s)
          print(packet)
          
          if args["power"] == "on" or  :
            if packet == power_on
              print("camera already powered on")
              power = True
            else : 
              serial_port.write(Commands.PowerOn)
              print("camera on !")
              power = True
          
          if args["power"] == "off" :
            if packet == power_off :
              print("camera already powered off")
              power = True
            else :
              serial_port.write(Commands.PowerOff)
            
          finished_packet = True
        
        else :
          packet.append(s)
          
        if s == "\r".encode():
          serial_port.write("\n".encode())
          
except KeyboardInterrupt:
    serial_port.write(Commands.ZoomStop)
    print("zoom stopped ...... Exiting Program")

#except Exception as exception_error:
    #print("Error occurred. Exiting Program")
    #print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass
