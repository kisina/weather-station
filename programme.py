# https://pyserial.readthedocs.io/en/latest/pyserial.html
# https://pyserial.readthedocs.io/en/latest/pyserial_api.html

import logging
from typing import Dict

import serial

# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(filename='example.log', level=logging.DEBUG)


class WeatherStation:
    """
    Class describing Weather Station
    """
    com_protocols_list: Dict[str, str] = {
        'A': 'ASCII, automatic',
        'a': 'ASCII, automatic with CRC',
        'P': 'ASCII, polled',
        'p': 'ASCII, polled, with CRC',
        'N': 'NMEA 0183 v3.0, automatic',
        'Q': 'NMEA 0183 v3.0, query (= polled)',
        'S': 'SDI-12 v1.3',
        'R': 'SDI-12 v1.3 continuous measurement',
    }

    serial_interface_list: Dict[int, str] = {
        1: 'SDI-12',
        2: 'RS-232',
        3: 'RS-485',
        4: 'RS-422',
    }

    parity_list = dict(O='Odd', E='Even', N='None')

    def __init__(self, serial_port, baudrate):
        print("OK station created")
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.ser = serial.Serial(self.serial_port)
        self.ser.baudrate = self.baudrate
        self.rain_peak_intensity = None
        self.hail_peak_intensity = None
        self.heating_temperature = None
        self.heating_voltage = None
        self.heating_state = None
        self.supply_voltage = None
        self.reference_voltage = None
        self.information_field = None
        
    def connect(self):
        if self.ser.is_open == False:
            self.ser.open()

        return self.ser.is_open

    def check_com_settings(self):
        self.ser.write(b'0XU\r\n')
        answer = self.ser.read_until()
        #answer_example = b'0XU,A=0,M=P,T=0,C=2,I=0,B=19200,D=8,P=N,S=1,L=25,N=WXT520,V=2.14\r\n'
        logging.info(answer)
        message_as_string = str(answer).replace("\\r\\n'", '').split(',')
        for elt in message_as_string:
            if 'A=' in elt: self.address = elt[2:]
            if 'M=' in elt: self.com_protocol = WeatherStation.com_protocols_list[elt[2:]]
            if 'C=' in elt: self.serial_interface = WeatherStation.serial_interface_list[int(elt[2:])]
            if 'I=' in elt: self.auto_repeat_interval = elt[2:]
            if 'B=' in elt: self.baud_rate = elt[2:]
            if 'D=' in elt: self.data_bits = elt[2:]
            if 'P=' in elt: self.parity = WeatherStation.parity_list[elt[2:]]
            if 'S=' in elt: self.stop_bits = elt[2:]
            if 'L=' in elt: self.line_delay = elt[2:]
            if 'N=' in elt: self.device_name = elt[2:]
            if 'V=' in elt: self.software_version = elt[2:]

        self.auto_repeat_interval = "no automatic repeat" if self.auto_repeat_interval == '0' else f"every {self.auto_repeat_interval} seconds"

        return True

    def __str__(self):
        return f"Weather station parameters:" \
               f"-Device Name: {self.device_name}\n" \
               f"-Address {self.address}\n" \
               f"-Communication protocol is: {self.com_protocol}\n" \
               f"-Serial Interface Protocol: {self.serial_interface}\n" \
               f"-Auto repeat: {self.auto_repeat_interval}\n" \
               f"-Baud rate: {self.baud_rate}\n" \
               f"-Data bits: {self.data_bits}\n" \
               f"-Parity: {self.parity}\n" \
               f"-Stop bits: {self.stop_bits}\n" \
               f"-line delay (for RS-485): {self.line_delay}\n" \
               f"-Software version: {self.software_version}"

    def wind_data_message(self):
        self.ser.write(b'0R1\r\n')
        answer = self.ser.read_until()
        logging.info(answer)
        message_as_string = str(answer).replace("\\r\\n'", '').split(',')
        for elt in message_as_string:
            if 'Dn=' in elt: self.wind_direction_min = int(elt[3:-1])
            if 'Dm=' in elt: self.wind_direction_avg = int(elt[3:-1])
            if 'Dx=' in elt: self.wind_direction_max = int(elt[3:-1])
            if 'Sn=' in elt: self.wind_speed_min = float(elt[3:-1])
            if 'Sm=' in elt: self.wind_speed_avg = float(elt[3:-1])
            if 'Sx=' in elt: self.wind_speed_max = float(elt[3:-1])
        return f"Dn={self.wind_direction_min} m/s\n" \
               f"Dm={self.wind_direction_avg} m/s\n" \
               f"Dx={self.wind_direction_max} m/s\n" \
               f"Sn={self.wind_speed_min} °\n" \
               f"Sm={self.wind_speed_avg} °\n" \
               f"Sx={self.wind_speed_max} °\n"

    def pressure_temperature_humidity_data_message(self):
        self.ser.write(b'0R2\r\n')
        answer = self.ser.read_until()
        logging.info(answer)
        message_as_string = str(answer).replace("\\r\\n'", '').split(',')
        for elt in message_as_string:
            if 'Ta=' in elt: self.air_temperature = float(elt[3:-1])
            if 'Ua=' in elt: self.relative_humidity = float(elt[3:-1])
            if 'Pa=' in elt: self.air_pressure = float(elt[3:-1])
        return f"Ta={self.air_temperature} °C\n" \
               f"Ua={self.relative_humidity} %RH\n" \
               f"Pa={self.air_pressure} hPa\n"

    def precipitation_data_message(self):
        self.ser.write(b'0R3\r\n')
        answer = self.ser.read_until()
        logging.info(answer)
        message_as_string = str(answer).replace("\\r\\n'", '').split(',')
        for elt in message_as_string:
            if 'Rc=' in elt: self.rain_accumulation = float(elt[3:-1])
            if 'Rd=' in elt: self.rain_duration = float(elt[3:-1])
            if 'Ri=' in elt: self.rain_intensity = float(elt[3:-1])
            if 'Hc=' in elt: self.hail_accumulation = float(elt[3:-1])
            if 'Hd=' in elt: self.hail_duration = float(elt[3:-1])
            if 'Hi=' in elt: self.hail_intensity = float(elt[3:-1])
            if 'Rp=' in elt: self.rain_peak_intensity = float(elt[3:-1])
            if 'Hp=' in elt: self.hail_peak_intensity = float(elt[3:-1])
        return f"Rc={self.rain_accumulation} mm\n" \
               f"Rd={self.rain_duration} s\n" \
               f"Ri={self.rain_intensity} mm/h\n" \
               f"Hc={self.hail_accumulation} hits/cm²\n"\
               f"Hd={self.hail_duration} s\n" \
               f"Hi={self.hail_intensity} hits/cm²h\n" \
               f"Rp={self.rain_peak_intensity} mm/h\n" \
               f"Hp={self.hail_peak_intensity} hits/cm²\n"

    def supervisor_data_message(self):
        self.ser.write(b'0R5\r\n')
        answer = self.ser.read_until()
        logging.info(answer)
        message_as_string = str(answer).replace("\\r\\n'", '').split(',')
        for elt in message_as_string:
            logging.info(elt)
            if 'Th=' in elt: self.heating_temperature = float(elt[3:-1])
            if 'Vh=' in elt: self.heating_voltage = float(elt[3:-1])
            if 'Heating=' in elt: self.heating_state = elt[-1]
            if 'Vs=' in elt: self.supply_voltage = float(elt[3:-1])
            if 'Vr=' in elt: self.reference_voltage = float(elt[3:-1])
            if 'Id=' in elt: self.information_field = elt[3:]
        return f"Th={self.heating_temperature} °C\n" \
               f"Vh={self.heating_voltage} V\n" \
               f"Heating={self.heating_state}\n" \
               f"Vs={self.supply_voltage} V\n"\
               f"Vr={self.reference_voltage} V\n" \
               f"Id={self.information_field}\n"

    def acknowledge_active_command(self):
        self.ser.write(b'0\r\n')
        answer = self.ser.read_until()
        logging.info(f"Answer from the device after acknowledge command: {answer}")
        test = answer==b'0\r\n'
        logging.info(f"Result from acknowledge active command{test}")
        return test

    def precipitation_sensor_checking_the_settings(self):
        self.ser.write(b'0RU\r\n')
        answer = self.ser.read_until()
        logging.info(f"Settings of the precipitation sensor: {answer}")
        return answer

    def precipitation_sensor_changing_the_settings(self, parameters):
        message = b'0RU'
        for attr, value in parameters.items():
            if attr in ['R']:#, 'I', 'U', 'S', 'M', 'Z', 'X', 'Y']:
                message += b',' + attr.encode() + b'=' + value
        """self.ser.write(b'0RU\r\n')
        answer = self.ser.read_until()
        logging.info(f"Settings of the precipitation sensor: {answer}")
        """
        message += b'\r\n'
        self.ser.write(message)
        answer = self.ser.read_until()
        check = answer == message
        if check:
            logging.info("Parameters changed successfully")
        else:
            logging.info("Error during parameters change")
        return check





weather_station = WeatherStation('/dev/ttyUSB0', 19200)

print("Connection...")
print(weather_station.connect())
print(weather_station.check_com_settings())
print(weather_station)

print("\nTesting wind")
print(weather_station.wind_data_message())

print("\nTesting pressure, temperature and humidity")
print(weather_station.pressure_temperature_humidity_data_message())

print("\nTesting precipitation")
print(weather_station.precipitation_data_message())

print("Testing supervisor message")
print(weather_station.supervisor_data_message())

print("Testing acknowledge")
weather_station.acknowledge_active_command()

print("Check settings")
weather_station.precipitation_sensor_checking_the_settings()

print("Test change settings")
parameters = {
    'R': b'11111111&11111111',
    'I': b'60',
    'U': b'M',
    'S': b'M',
    'M': b'R',
    'Z': b'M',
    'X': b'10000',
    'Y': b'100'
}
print(weather_station.precipitation_sensor_changing_the_settings(parameters))

"""ser.write(b'0XU\r\n')
answer = ser.read_until()
answer_example = b'0XU,A=0,M=P,T=0,C=2,I=0,B=19200,D=8,P=N,S=1,L=25,N=WXT520,V=2.14\r\n'
print(f'Answer: {answer}')
logging.warning(answer)
weather_station.decode_message_settings(answer)

print(weather_station)

ser.write(b'0R1\r\n')
answer = ser.read_until()
print(f'Answer: {answer}')"""