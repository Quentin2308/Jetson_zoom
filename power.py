# sans paramètre a caméra essaie de s'allumer
# allumage de la camera : sudo python3 power.py -p on 
# extinction de la camera : sudo python3 power.py -p off

import time
import serial
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--power", type=str,
    help="camera power")
args = vars(ap.parse_args())

print("UART Program")
print("NVIDIA Jetson Nano Developer Kit")

power_on = [b'\x90', b'P', b'\x02', b'\xff']
power_off = [b'\x90', b'P', b'\x03', b'\xff']

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
  #serial_port.write(Commands.PowerOn)      
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
          #print(packet)
          
          if args["power"] == "on" or not args.get("power",False) :
            if packet == power_on :
              print("camera already powered on")
              power = True
            elif packet == power_off : 
              serial_port.write(Commands.PowerOn)
              print("camera on !")
              power = True
          
          if args["power"] == "off" :
            if packet == power_off :
              print("camera already powered off")
              power = True
            elif packet == power_on :
              serial_port.write(Commands.PowerOff)
              print("camera power off !")
              power = True
                
          finished_packet = True
        
        else :
          packet.append(s)
          
        if s == "\r".encode():
          serial_port.write("\n".encode())
          
except KeyboardInterrupt:
    
    print("...... Exiting Program")

#except Exception as exception_error:
    #print("Error occurred. Exiting Program")
    #print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass
