'''
Copyright (C) 2022 Francesco Paparella, Pedro Velasquez, Bimarsha Adhikari 

This file is part of "ACCESS IOT Stations".

"ACCESS IOT Stations" is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

"ACCESS IOT Stations" is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
"ACCESS IOT Stations". If not, see <https://www.gnu.org/licenses/>.
'''

##########

import ACCESS_station_lib as access
from adafruit_extended_bus import ExtendedI2C as I2C
import json

##########

'''
this file should define 2 things
sensors: list with ALL the sensors of all types
            Any beseecher sensor connected to the station must be appended to
            this list
gps: unlike the sensors, the gps will be a unique variable with the gps
beseecher.

When initializing sensors, ALWAYS use a try-except block in case the RPi
fails to start the sensors at boot. The error beseecher class will store any
error information that comes up and will allow data-collection to report on
the error.
'''

# try building gps, GPS sensor is critical point of failure for system
try:
    gps = access.GPSbeseecherGPIO()  # only 1 GPS
except Exception:
    gps = access.ErrorBeseecher('gps', 'gps', 'Error initializing GPS at boot')

# list to keep all sensors
sensors = []

# retreive the sensor configuration from the station.config file
with open("station.config") as station:
    station_config = json.loads(station.read()) 

for sensor in station_config:
    if sensor == "particulate_matter":
        for pm_sensor in station_config[sensor]:
            if "ports" in pm_sensor:
                for port in pm_sensor["ports"]:
                    try:
                        sensors.append(access.NEXTPMbeseecher(port=port))
                    except Exception as e:
                        sensors.append(access.ErrorBeseecher(
                            'particulate_matter', 'nextpm', str(e)))
            elif "i2c_buses" in pm_sensor:
                sens_type = pm_sensor["type"]
                for i2c_bus in pm_sensor["i2c_buses"]:
                    i2c_num = i2c_bus[0]
                try:
                    exec(f"sensors.append(access.{sens_type.upper()}beseecher(i2c_bus_number=i2c_num))")

                except Exception as e:
                    error_msg = str(e)
                    sensors.append(access.ErrorBeseecher(
                        sensor, f'{sens_type} {i2c_num}', error_msg))

    if sensor in ["air_sensor", "co2_sensor"]:
        for sens in station_config[sensor]:
            sens_type = sens["type"]
            for i2c_bus in sens["i2c_buses"]:
                i2c_num = i2c_bus[0]
                if len(i2c_bus) == 2:
                    addr = i2c_bus[1]
                try:
                    if len(i2c_bus) == 2:
                        exec(
                            f"sensors.append(access.{sens_type.upper()}beseecher(i2c=I2C(i2c_num), address = addr))")
                    else:
                        exec(
                            f"sensors.append(access.{sens_type.upper()}beseecher(i2c=I2C(i2c_num)))")

                except Exception as e:
                    error_msg = str(e)
                    sensors.append(access.ErrorBeseecher(
                        sensor, f'{sens_type} {i2c_num} {addr}', error_msg))

'''
set up indeces for all sensors

DO NOT MODIFY THIS PART, ONLY MODIFY SENSOR DECLARATIONS ABOVE

these index set up is necessary for multithreading
we don't know which thread will finish first, these indeces will make sure
    the order of sensors is kept (we want the data collected by sensor i to
    always be the ith index in the data file)
'''
indeces = {}
for sensor in sensors:
    indeces[sensor.SENSOR] = indeces.get(sensor.SENSOR, -1) + 1
    sensor.index = indeces[sensor.SENSOR]