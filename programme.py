# https://pyserial.readthedocs.io/en/latest/pyserial.html
# https://pyserial.readthedocs.io/en/latest/pyserial_api.html


from app.WeatherStation import WeatherStation

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
parameters_precipitation = {
    'R': b'11111111&11111111',  # Parameter selection
    'I': b'60',  # Update interval: 1 ... 3600 seconds. This interval is valid only if the [M] field is = T
    'U': b'M',  # Precipitation units
    'S': b'M',  # Hail units
    'M': b'R',  # Autosend mode: R = precipitation on/off, C = tipping bucket, T = time based
    'Z': b'M',  # Counter reset: M = manual, A = automatic, L=limit, Y = immediate
    'X': b'10000',  # Rain accumulation limit : 100...65535
    'Y': b'10000' # Hail accumulation limit : 100...65535
}
print(weather_station.precipitation_sensor_changing_the_settings(parameters_precipitation))

print("Test change settings on supervisor")
parameters_supervisor = {
    'R': b'11111111&11111111',  # Parameter selection
    'I': b'60',  # Update interval:1-3600 seconds. When heating is enabled the update interval is forced to 15seconds.
    'S': b'Y',  # Error messaging: Y = enabled, N = disabled
    'H': b'Y',  # Heating control enable: Y = enabled, N = disabled
}
print(weather_station.supervisor_message_changing_the_settings(parameters_supervisor))

print("Test change settings on TPH")
parameters_tph = {
    'R': b'11111000&11110000',  # Parameter selection
    # 'R': b'00000000&00000000',  # Parameter selection
    'I': b'60',  # Update interval: 1 ... 3600 seconds
    'P': b'H',  # Pressure unit: H = hPa, P = Pascal, B = bar, M = mmHg, I = inHg
    'T': b'C',  # Temperature unit: C = Celsius, F = Fahrenheit
}
print(weather_station.pressure_temperature_humidity_changing_the_settings(parameters_tph))

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
