#!/usr/bin/python

# TODO:
#       You have to think to translate the mm space that directly translates to radians to the 3D space position of the robot arm.
#       Include Sensor class to obtain information. Think about doing it with other thread, asyncio
#           Accelerometer gyroscope
#           Encoder

import serial
from serial.tools.list_ports_posix import comports
from stepper_motors import Nema17StepperMotor, Mitsumi55StepperMotor 
import time
debug=True 


def send_command(ser,cmd):
    ''' Sends info to the Arduino and waits 1ms to response.
    Returns response.'''
    ser.write((cmd+'\n').encode())
    if debug:print('TO ->',cmd.replace('\r\n','\r\n\t\t'))
    time.sleep(0.01)
    response_u =  b''.join(ser.readlines())
    response = response_u.decode() 
    if debug and response != '\r\n' :print('FROM <-',response.replace('\r\n','\r\n\t\t'))
    return(response)

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


class ControllerArduino():
    def __init__(self,
            comport,
            name,
            powersupply=12#in volts
            ):
        self.comport = comport
        self.powersupply = powersupply
        self.ser = None
        self.name = name
        self.motors =dict()
        self.sensors = dict()
        self.connect()

    def appendMotor(self,motor,position):
        if position in ['x','y','z']:
            self.motors[position] = motor
            conf = motor.getconfig()
            if position == 'x':
                self.sendcmd('$100=%.3f'%conf['step_mm'])
                self.sendcmd('$110=%.3f'%conf['max_rate'])
                self.sendcmd('$120=%.3f'%conf['accel'])
            if position == 'y':
                self.sendcmd('$101=%.3f'%conf['step_mm'])
                self.sendcmd('$111=%.3f'%conf['max_rate'])
                self.sendcmd('$121=%.3f'%conf['accel'])
            if position == 'z':
                self.sendcmd('$102=%.3f'%conf['step_mm'])
                self.sendcmd('$112=%.3f'%conf['max_rate'])
                self.sendcmd('$122=%.3f'%conf['accel'])
        else:
            raise Exception

    def appedSensor(self,sensor,position):
        if position in ['x','y','z']:
            self.sensors[position] = sensor 
            conf = sensor.getconfig()
            if position == 'x':
                pass
            if position == 'y':
                pass
            if position == 'z':
                pass 
        else:
            raise Exception

       

    def connect(self):
        self.ser = serial.Serial(self.comport,115200,timeout=0)
        if debug: print(self.name,'Starting system in: ',self.comport)
        
    def disconnect(self):
        self.sendcmd('$1=1')
        self.sendcmd('$1=0')
        self.ser.close()

    def softstop(self):
        return sendcmd('!')

    def resumeoperation(self):
        return self.sendcmd('~')

    def currentstate(self):
        #need to parse
        return self.sendcmd('?')
    
    def incrementPosition(self,x,y,z):
        return self.sendcmd('G91 G0 x%sy%sz%s'%(x,y,z))

    def setPosition(self,x,y,z):
        return self.sendcmd('g00 x%sy%sz%s'%(x,y,z))
    
    def sendcmd(self,cmd):
        return send_command(self.ser,cmd)


if __name__ == '__main__':
    print('cmps','stpm')
    cmps = get_port_name()
    ctrl = ControllerArduino(cmps,'ctrl0')
    m55stpm =Mitsumi55StepperMotor()
    nema17 = Nema17StepperMotor()
    time.sleep(2)
    ctrl.appendMotor(nema17,'x')
    ctrl.appendMotor(m55stpm,'z')





