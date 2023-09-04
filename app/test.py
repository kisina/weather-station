from WeatherStation import WeatherStation

weather_station = WeatherStation('/dev/ttyUSB0', 19200)

weather_station.connect()
#a = weather_station.check_com_settings()
#print(a)

a = weather_station.pressure_temperature_humidity_data_message()

print(a)

a = weather_station.wind_sensor_checking_the_settings()
print(a)