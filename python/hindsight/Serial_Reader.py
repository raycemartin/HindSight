import serial
import time
import csv

data_export = []

def readserial(comport, baudrate, timestamp=False):

    ser = serial.Serial(comport, baudrate, timeout=0.1)         # 1/timeout is the frequency at which the port is read

    while True:

        data = ser.readline().decode().strip()
        data_export.append(data)
        if data and timestamp:
            timestamp = time.time()
            print(f'{timestamp} > {data}')
        elif data:
            print(data)
    
    
if __name__ == '__main__':

    readserial('COM4', 9600, True)                          # COM port, Baudrate, Show timestamp