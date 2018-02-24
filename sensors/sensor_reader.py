#!/usr/bin/python
# Compatibility with general_sensor.ino

from serial import Serial 
from serial.tools.list_ports_posix import comports
from debug import debug
import time 

def get_port_name():
    ''' Displays information to terminal to led the user select the comport (Arduino USB connection)'''
    cps = comports()
    print('Printing devices available.')
    if len(cps)==0:
        print('Error: Seems empty ...')
        print('Exiting...')
        exit()
    for cp, i  in enumerate(cps):
        print(str(i)+')',cp)
    print('Select the device.\n>',end='')
    us = input()
    device = 0
    if us !='':
        try:
            device=int(us)
        except:
            print('Not a number, selecting ', device,cps[device].device )
    return cps[device].device

def send_command(ser,cmd):
    ''' Sends info to the Arduino and waits 1ms to response.
        Returns response.'''
    ser.write((cmd+'\r\n').encode())
    if debug:print('TO ->',cmd.replace('\r\n','\r\n\t\t'))
    time.sleep(0.01)


class SensorReader():
    def __init__(self,serialport):
        ''' Serial port already opened'''
        self.serport = serialport
        self.nbline = ""
        self.ser = Serial(serialport,115200)#,timeout=0)
        if debug: print("Serial opened.")

    def sendcmd(self,cmd):
        return send_command(self.ser,cmd)

    def takeSample(self):
        return self.sendcmd('r1') 
    
    def takeSamples(self):
        return self.sendcmd('r')

    def takeNSamples(self,n):
        n = int(n)
        return self.sendcmd('r%s'%n)

    def takePeriodicSamples(self,microseconds):
        n = int(microseconds)
        return self.sendcmd('m%s'%microseconds)
    
    def getNBLine(self):
        waiting = self.ser.inWaiting()
        if waiting>0:
            self.nbline += self.ser.read(waiting).decode('ascii')
        if '\r\n' in self.nbline :
            position = self.nbline.rfind('\r\n')+2
            line = self.nbline[0:position]
            if debug: print('FROM <- ',line)
            self.nbline = self.nbline[position:-1]
            return line
        return None

        


class Encoder(SensorReader):
    pass


class Gyroscope(SensorReader):
    pass 


