#https://pyserial.readthedocs.io/en/latest/pyserial.html
#https://pyserial.readthedocs.io/en/latest/pyserial_api.html

import logging
import serial
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 19200
if ser.is_open == False
	ser.open()
ser.is_open
ser.write(b'0XU\r\n')
answer = ser.read_until()
print('test')
logging.warning(answer)
