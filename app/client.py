import streamlit as st
import pandas as pd
from WeatherStation import WeatherStation
import pandas as pd
import numpy as np

weather_station = WeatherStation('/dev/ttyUSB0', 19200)

weather_station.connect()
weather_station.check_com_settings()

st.write("""
# ⛅ Local client for the weather station ⛅

## Communication settings
""")

d = {
    "Device name": f"{weather_station.device_name}",
    "Address": f"{weather_station.address}",
    "Serial interface": f"{weather_station.serial_interface}",
    "Repeat interval": f"{weather_station.auto_repeat_interval}",
    "Baud rate": f"{weather_station.baud_rate}",
    "Data bits": f"{weather_station.data_bits}",
    "Parity": f"{weather_station.parity}",
    "Stop bits": f"{weather_station.stop_bits}",
    "RS-485 line delay": f"{weather_station.line_delay}",
    "Software version": f"{weather_station.software_version}",
}

b = np.array(list(d.items()))

st.dataframe(b, column_config={
    1: st.column_config.TextColumn(label="Parameters"),
    2: st.column_config.TextColumn(label="Value", width='medium'),
})


with st.form("Wind sensor settings"):
    st.write("## Wind sensor settings")
    weather_station.wind_sensor_checking_the_settings()

    df = pd.DataFrame(
        [
            {"parameters": "W-Wind update interval (seconds)", "value": weather_station.wind_update_interval},
            {"parameters": "W-Wind averaging time (seconds)", "value": weather_station.wind_averaging_time},
            {"parameters": "W-Wind direction offset (°)", "value": weather_station.wind_direction_offset},
            {"parameters": "W-Wind sampling rate (Hz)", "value": weather_station.wind_sampling_rate},
        ]
    )
    edited_df = st.data_editor(df, hide_index=True)

    wind_update_interval = edited_df[edited_df['parameters'] == 'W-Wind update interval (seconds)']["value"].values.tolist()[0]
    wind_averaging_time = edited_df[edited_df['parameters'] == 'W-Wind averaging time (seconds)']["value"].values.tolist()[0]
    wind_direction_offset = edited_df[edited_df['parameters'] == 'W-Wind direction offset (°)']["value"].values.tolist()[0]
    wind_sampling_rate = edited_df[edited_df['parameters'] == 'W-Wind sampling rate (Hz)']["value"].values.tolist()[0]

    wind_speed_units_list = [key + '-' + weather_station.wind_speed_units_list[key] for key in weather_station.wind_speed_units_list]
    wind_speed_units_list.sort()
    if weather_station.wind_speed_unit == 'km/h':
        index = 0
    elif weather_station.wind_speed_unit == 'm/s':
        index = 1
    elif weather_station.wind_speed_unit == 'knots':
        index = 2
    elif weather_station.wind_speed_unit == 'mph':
        index = 3
    wind_speed_unit = st.selectbox(
        'Unit for wind speed',
        wind_speed_units_list,
        index=index)
    wind_speed_unit = weather_station.wind_speed_units_list[wind_speed_unit[0]]

    index = 0 if weather_station.wind_speed_calculation_mode == 1 else 1
    wind_speed_calculation_mode = st.selectbox(
        'Wind speed calculation_mode',
        ['1','3'],
        index=index)

    index = 0 if weather_station.nmea_wind_formatter == 'T' else 1
    nmea_wind_formatter = st.selectbox(
        'NMEA wind formatter',
        ['T-XDR', 'W-MWV'],
        index=index)

    st.write("### Parameters to be transmitted")
    [dn, dm, dx, sn, sm, sx] = [bool(int(x)) for x in weather_station.wind_parameters[0:6]]
    dn = st.toggle("Direction minimum", value=dn)
    dm = st.toggle("Direction average", value=dm)
    dx = st.toggle("Direction maximum", value=dx)
    sn = st.toggle("Speed minimum", value=sn)
    sm = st.toggle("Speed average", value=sm)
    sx = st.toggle("Speed maximum", value=sx)
    wind_parameters = [dn, dm, dx, sn, sm, sx, False, False]
    wind_parameters = ''.join('1' if b else '0' for b in wind_parameters)
    wind_parameters = wind_parameters + '&' + wind_parameters

    st.write(f"W-Wind parameters: {weather_station.wind_parameters}")
    st.write(f"W-Wind parameters: {wind_parameters}")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        parameters = {
            'R': bytes(wind_parameters, 'utf-8'),
            'I': bytes(str(wind_update_interval), 'utf-8'),
            'A': bytes(str(wind_averaging_time), 'utf-8'),
            'G': bytes(wind_speed_calculation_mode, 'utf-8'),
            'U': bytes(wind_speed_unit, 'utf-8'),
            'D': bytes(str(wind_direction_offset), 'utf-8'),
            'N': bytes(nmea_wind_formatter, 'utf-8'),
            'F': bytes(str(wind_sampling_rate), 'utf-8'),
        }
        print("tadam")
        print(parameters)
        test = weather_station.wind_sensor_changing_the_settings(parameters)
        print(test)




st.write("## Measurements")
weather_station.wind_data_message()
weather_station.pressure_temperature_humidity_data_message()
d = {
    "W-Wind direction min (°)": f"{weather_station.wind_direction_min}",
    "W-Wind direction avg (°)": f"{weather_station.wind_direction_avg}",
    "W-Wind direction max (°)": f"{weather_station.wind_direction_max}",
    "W-Wind speed min (m/s)": f"{weather_station.wind_speed_min}",
    "W-Wind speed avg (m/s)": f"{weather_station.wind_speed_avg}",
    "W-Wind speed max (m/s)": f"{weather_station.wind_speed_max}",
    "PTH-Air Temperature (°C)": f"{weather_station.air_temperature}",
    "PTH-Relative humidity (% RH)": f"{weather_station.relative_humidity}",
    "PTH-Air pressure (hPa)": f"{weather_station.air_pressure}",
}
b = np.array(list(d.items()))
st.dataframe(b, column_config={
    1: st.column_config.TextColumn(label="Parameters", width='medium'),
    2: st.column_config.TextColumn(label="Value", width='medium'),
})

weather_station.pressure_temperature_humidity_data_message()

st.write("## Just for test")

st.toggle("test")

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option