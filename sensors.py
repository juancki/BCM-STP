#!/usr/bin/python

# Implementation of sensors 
#       gyroscope and accelerometer
#       encoder

import datetime 

class Sensor():
    def measurePhysicalValue():
        ''' getPhysicalValue has to return strictly the value obtained from the sensor. '''
        raise NotImplementedError()

    def measure():
        '''measure() reads the information of the sensor and returns a calibrated mapped value. '''
        raise NotImplementedError()
    
    def mapper(x):
        ''' Returns the calibrated measurement.'''
        raise NotImplementedError()
    def __init__(self,units):
        self.is_calibrated = False
        self.units = units

class Sampler():
    def __init__(self,sensor):
        self.sensor = sensor
        self.buffer

    def takeNsamples(self,n):
        a = []*n
        for i in range(n):
            m = self.sensor.measure()
            a[i]=Sample(m,datetime.datetime.now())
        self.buffer = a
        return a
    
    def takeSamples(self,seconds):
        a = []*seconds*10000
        s = datetime.datetime.now()
        i = 0
        while (s-datetime.datetime.now()-s).total_seconds()<seconds :
            m = self.sensor.measure()
            a[i]=(m,datetime.datetime.now())
            i+=1
            if i>=len(a)-2:
                b = []*(len(a)+10000)
                b[0:i]=a
                a = b.copy()
                del b
        return a



