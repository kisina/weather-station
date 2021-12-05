#https://pyserial.readthedocs.io/en/latest/pyserial.html
#https://pyserial.readthedocs.io/en/latest/pyserial_api.html




import logging
import serial
#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 19200
if not ser.is_open:
	ser.open()
else:
	logging.info("Serial port is opened")
ser.is_open
ser.write(b'0XU\r\n')
answer = ser.read_until()
print('Answer:')
print(answer)
logging.info(answer)

ser.write(b'0R1\r\n')
answer = ser.read_until()
print('Answer:')
print(answer)
logging.info(answer)

#test:
#b'0XU,A=0,M=P,T=0,C=2,I=0,B=19200,D=8,P=N,S=1,L=25,N=WXT520,V=2.14\r\n'
#b'0R1,Dn=167D,Dm=174D,Dx=186D,Sn=0.9M,Sm=1.2M,Sx=1.5M\r\n'


answer = answer.decode("utf-8")
answer = answer.replace("\r\n","")
print(answer.split(','))

