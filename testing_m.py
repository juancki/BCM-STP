from serial import Serial
from serial.tools.list_ports_posix import comports
import time
debug = True

## https://www.staticboards.es/blog/dominar-motor-paso-a-paso-con-grbl/
## https://www.youtube.com/watch?v=KXyS63nO_rU 
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
    ser.write((cmd+'\n').encode())
    if debug:print('TO ->',cmd.replace('\r\n','\r\n\t\t'))
    time.sleep(0.01)
    response_u =  b''.join(ser.readlines())
    response = response_u.decode() 
    if debug and response != '\r\n' :print('FROM <-',response.replace('\r\n','\r\n\t\t'))
    return(response)


def velocitytest(ser):
    send_command(ser,'$112=100')
    send_command(ser,'g01 z0')
    for i in range(1,4):
        print('To zero position')
        ## first slowly
        print('To 10 position')
        send_command(ser,'g00 z.5 f'+str(i))    
        time.sleep(2)
        send_command(ser,'g00 z-.5 f'+str(2*i))
        time.sleep(2)
        send_command(ser,'$112='+str(100+25*i))
    send_command(ser,'g01 z0')

if __name__  == "__main__":
    print('Starting system...')
    motor = get_port_name()
    print()
    print('Motor at ',motor)
    ser = Serial(motor,115200,timeout=0) # serial connection to arduino GRBL
    print('Starting connection to', motor)
    time.sleep(2)
    print(send_command(ser,'?'))
    #send_command(ser,'$112=50')
    velocitytest(ser) 

