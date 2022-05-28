#https://pyserial.readthedocs.io/en/latest/pyserial.html
#https://pyserial.readthedocs.io/en/latest/pyserial_api.html

import logging
import serial
#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(filename='example.log', level=logging.DEBUG)


class WeatherStation:
	"""
	Class describing Weather Station
	"""
	com_protocols = {
		'A': 'ASCII, automatic',
		'a': 'ASCII, automatic with CRC',
		'P': 'ASCII, polled',
		'p': 'ASCII, polled, with CRC',
		'N': 'NMEA 0183 v3.0, automatic',
		'Q': 'NMEA 0183 v3.0, query (= polled)',
		'S': 'SDI-12 v1.3',
		'R': 'SDI-12 v1.3 continuous measurement',
		}

	def __init__(self):
		print("OK station created")

	def decode_message(self, message):
		#A = re.search(r"A=\S,", message)
		message_as_string = str(message).replace("\\r\\n'",'').split(',')
		for elt in message_as_string:
			if 'A=' in elt: self.address = elt[2:]
			if 'M=' in elt: self.com_protocol = WeatherStation.com_protocols[elt[2:]]
			if 'C=' in elt: self.serial_interface = elt[2:]
			if 'I=' in elt: self.auto_repeat_interval = elt[2:]
			if 'B=' in elt: self.baud_rate = elt[2:]
			if 'D=' in elt: self.data_bits = elt[2:]
			if 'P=' in elt: self.parity = elt[2:]
			if 'S=' in elt: self.stop_bits = elt[2:]
			if 'L=' in elt: self.line_delay = elt[2:]
			if 'N=' in elt: self.device_name = elt[2:]
			if 'V=' in elt: self.software_version = elt[2:]

	def __str__(self):
		return f"Device Name: {self.device_name}\n" \
			   f"@adress {self.address}" \
			   f"Communication protocol is: {self.com_protocol}"




weather_station = WeatherStation()

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 19200
if ser.is_open == False:
	ser.open()
ser.is_open
ser.write(b'0XU\r\n')
answer = ser.read_until()
answer_example = b'0XU,A=0,M=P,T=0,C=2,I=0,B=19200,D=8,P=N,S=1,L=25,N=WXT520,V=2.14\r\n'
print(f'Answer: {answer}')
logging.warning(answer)
weather_station.decode_message(answer)

print(weather_station)


