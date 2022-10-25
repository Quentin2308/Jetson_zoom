#!/usr/bin/python3
import time
import serial

print("UART Program")
print("NVIDIA Jetson Nano Developer Kit")

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



print(Commands.adress_set)

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
    
    temps=time.time() #stockage du tps actuel
    
    while (time.time()-temps<5000): #5 secondes
        serial_port.write(Commands.ZoomTele)
        if serial_port.inWaiting() > 0:
            data = serial_port.read()
            print(data)
            
            #serial_port.write(data)
            # if we get a carriage return, add a line feed too
            # \r is a carriage return; \n is a line feed
            # This is to help the tty program on the other end 
            # Windows is \r\n for carriage return, line feed
            # Macintosh and Linux use \n
            if data == "\r".encode():
                # For Windows boxen on the other end
                serial_port.write("\n".encode())
    serial_port.write(Commands.ZoomStop)
    

except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    pass
