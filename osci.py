#!/usr/bin/python
# -*- coding: utf-8 -*-
"""PiPyADC: Example file for class ADS1256 in module pipyadc:

ADS1256 cycling through eight input channels.

Hardware: Waveshare ADS1256 board interfaced to the Raspberry Pi 3
 
Ulrich Lukas 2017-03-10
"""
import sys
#import serial
import json
from ADS1256_definitions import *
from pipyadc import ADS1256
import asyncore, socket, time
import numpy as np 
from collections import deque
from SoftOscilloscope import SocketClientPlot
from multiprocessing import Process

data = np.linspace(-np.pi, np.pi, 50)

# Input pin for the potentiometer on the Waveshare Precision ADC board:
POTI = POS_AIN0|NEG_AINCOM
# Light dependant resistor of the same board:
LDR  = POS_AIN1|NEG_AINCOM
# The other external input screw terminals of the Waveshare board:
EXT2, EXT3, EXT4 = POS_AIN2|NEG_AINCOM, POS_AIN3|NEG_AINCOM, POS_AIN4|NEG_AINCOM
EXT5, EXT6, EXT7 = POS_AIN5|NEG_AINCOM, POS_AIN6|NEG_AINCOM, POS_AIN7|NEG_AINCOM

# You can connect any pin as well to the positive as to the negative ADC input.
# The following reads the voltage of the potentiometer with negative polarity.
# The ADC reading should be identical to that of the POTI channel, but negative.
POTI_INVERTED = POS_AINCOM|NEG_AIN0

# For fun, connect both ADC inputs to the same physical input pin.
# The ADC should always read a value close to zero for this.
SHORT_CIRCUIT = POS_AIN0|NEG_AIN0

# Specify here an arbitrary length list (tuple) of arbitrary input channel pair
# eight-bit code values to scan sequentially from index 0 to last.
# Eight channels fit on the screen nicely for this example..
CH_SEQUENCE = (POTI, LDR, EXT2, EXT3, EXT4, EXT7, POTI_INVERTED, SHORT_CIRCUIT)
################################################################################


class Server(asyncore.dispatcher):   
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bind(address)
        self.listen(5)
        return 
        
    def handle_accept(self):
	ads = ADS1256()
	ads.cal_self()		
        global data
        client, addr = self.accept()
        print("Connected to " + str(addr))	
        while(1):
            try:
		raw_channels = ads.read_sequence(CH_SEQUENCE)
		voltages     = [i * ads.v_per_digit for i in raw_channels]
		ferguso = ','.join(map(str, voltages))
                client.send((ferguso + '\n').encode())
                data = np.roll(data, 1)
                time.sleep(0.05)
            except Exception as e:
                print(e)
                return
        
    def handle_close(self):
        self.close()
        print("Closing server.")


if __name__ == '__main__':
    address = ('localhost',9000)
    server = Server(address)
    try:
        print("Server listening on " + str(address))
        asyncore.loop(0.2, use_poll=True)
    except KeyboardInterrupt:
        print("Closing server.")
        server.close()
