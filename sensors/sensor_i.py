#!/usr/bin/python
# Compatibility with general_sensor.ino

from sensors import Sensor, Sampler
from serial import Serial 
from debug import debug
import time 


def sendcmd(ser,cmd):
    b_cmd = bytes(cmd)
    ito = ser.writeTimeout 
    r = ser.write(b_cmd)
    ser.flushOutput()
    ser.writeTimeout = ito
    return r


class SerialReader(Sampler):
    def __init__(self,serialport):
        ''' Serial port already opened'''
        self.serport = serialport
        self.ser = Serial(serialport,115200)#,timeout=0)
    
    def takeSample(self):
        if debug:print('TO -> 0x01')
        sendcmd(self.ser,[1])
        ln = self.ser.readline()
        if debug:print('FROM<-',ln)
        return int(ln)
    def takeNSamples(self):
        pass

    def takeSamples(self,seconds):
        if debug:print('TO -> 0xFF')
        self.ser.writeTimeout= 0
        sendcmd(self.ser,[0xff])
        t_init = time.time()
        result = []
        while True:
            if time.time()-t_init >seconds:break
            self.ser.timeout=0
            ln = self.ser.readline()
            if len(ln)!=0:result.append(int(ln))
            if debug and len(ln)!=0:print('FROM<-',ln)
        if debug:print('TO -> 0x00')
        sendcmd(self.ser,[0]) 

    def iTakeSamples(self,seconds):
        # catching previous state
        to = self.ser.timeout
        # Writing
        if debug:print('TO -> 0xFF')
        sendcmd(self.ser,[0xff])
        # Reading
        self.ser.timeout=seconds
        lns = self.ser.readlines()
        # Stop
        sendcmd(self.ser,[0]) 

        if debug:print('TO -> 0x00')       
        if debug and len(ln)!=0:print('FROM<-',lns)
        # Returning previous state
        # self.ser.timeout = to
        return [int(q) for q in lns]



class Encoder(Sensor):
    pass


class Gyroscope(Sensor):
    pass 


