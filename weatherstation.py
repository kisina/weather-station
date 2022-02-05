"""This module manages the connection with the weather station
"""

import serial
import logging


class WeatherStation:
    """This class manages the connection and the behavior of the weather station
    """
    def __init__(self, serial_port='/dev/ttyUSB0', baudrate=19200):
        """

        :type baudrate: connection baudrate
        """
        self.serial_port = serial_port
        self.baudrate = baudrate

    def connect(self):
        """Open the connection with the weather station"""
        try:
            ser = serial.Serial(self.serial_port)
            ser.baudrate = self.baudrate
        except:
            logging.info("Connection to the station has failed")
            return False

        if not ser.is_open:
            ser.open()
        else:
            logging.info("Serial port is already opened")

        if ser.is_open:
            ser.write(b'0XU\r\n')
            answer = ser.read_until()
            logging.info('Answer:')
            logging.info(answer)
            return True
        else:
            return False


station = WeatherStation()
print(station.connect())
