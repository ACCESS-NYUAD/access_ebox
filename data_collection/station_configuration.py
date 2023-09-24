'''

Copyright (C) 2023 Francesco Paparella, Bimarsha Adhikari 

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

import json

"""
The following 'sensors' dictionary allows us to specify the sensors and their 
respective connection settings. 

1. The keys of the sensors dictionary must represent sensor categories; eg. 
   "air_sensor", "co2_sensor", "particulate_matter".
2. Each category key holds a list of unique sensor types, eg. BME280, SCD30,
   NEXTPM. Each sensor type can be used to enlist multiple sensors of the 
   same type with different connection settings. 
3. Each sensor type must include a "type". Either "i2c_buses" or "ports"  
   should be the second key depending on the type of connection. 
      i.  Use "ports" with a list of ports in string format for UART 
          communication.
      ii. Use "i2c_buses" with a list of lists for I2C communication. Inner
          lists for I2C should have two elements (I2C number and address), 
          or one element (I2C bus number) in case of a default address. 
          Note than MS8607, SCD30 and SPS30 sensors ONLY accept I2C number as part
          of the inner list, DO NOT try to mention the address. Use 
          "i2cdetect -y <bus_number>" to find the address of the sensor 
          connected to the I2C bus. Default addresses for some I2C-based 
          sensors are: 
                BME280: 0x77 (0x76 if SDO pin is connected to GND)
                SCD30: 0x61

Below is an example of a possible sensor configuration with three sensor 
categories. Each category contains one or multiple different types of 
sensors with their respective communication configurations. 
"""
sensors = {
    "particulate_matter": [
        {
            "type": "NEXTPM",
            "ports": ["/dev/ttyAMA0", "/dev/ttyAMA2"]
        }],

    "air_sensor": [
        {
            "type": "BME280",
            "i2c_buses": [[1, 0x77], [2, 0x77]]
        }],
    "co2_sensor": [
        {
            "type": "SCD30",
            "i2c_buses": [[1], [2]]
        }] 
}

with open("station.config", "w") as file:
    json.dump(sensors, file, indent=4)