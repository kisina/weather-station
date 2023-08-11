import streamlit as st
import pandas as pd
from WeatherStation import WeatherStation
import pandas as pd
import numpy as np

weather_station = WeatherStation('/dev/ttyUSB0', 19200)

weather_station.connect()
weather_station.check_com_settings()

d={
    "Device name": f"{weather_station.device_name}",
    "Address": f"{weather_station.address}",
}

result = d.items()
d = list(result)



b = np.array(d)

b

st.dataframe(b, column_config={
    1: st.column_config.TextColumn(label="Parameters"),
    2: st.column_config.TextColumn(label="Value"),
})

"""weather_station.address
f"-Communication protocol is: {weather_station.com_protocol}\n" \
f"-Serial Interface Protocol: {weather_station.serial_interface}\n" \
f"-Auto repeat: {weather_station.auto_repeat_interval}\n" \
f"-Baud rate: {weather_station.baud_rate}\n" \
f"-Data bits: {weather_station.data_bits}\n" \
f"-Parity: {weather_station.parity}\n" \
f"-Stop bits: {weather_station.stop_bits}\n" \
f"-line delay (for RS-485): {weather_station.line_delay}\n" \
f"-Software version: {weather_station.software_version}"
"""

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option