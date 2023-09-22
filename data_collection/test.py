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

import threading
import sensors as sens 
from ACCESS_station_lib import Beseecher 
import time
import json 

##########

'''
This file will attempt to request measurements from all sensors
if it crashes at any point, it will log failure and let the user know

After testing all sensors, it will automatically create a config file for the
pi
This file is critical for the pi's "activation"
During setup, the Pi will send this file to the receiver to signal it is about
to start collecting data
'''

##########
data_saved = {} 
threads = [] 

def measure(sensor): 
    global data_saved 

    try: 
        if sensor.SENSOR == "particulate_matter": 
            data = sensor.measurePM_10_seconds()
        else: 
            data = sensor.measure() 
        print("Testing", sensor.SENSOR, sensor.index) 
        if sensor in data_saved: 
            data_saved[sensor].append(data)  
        else: 
            data_saved[sensor] = [data]
    except: 
        print(f"Error with {sensor}") 

def main():
    global threads 
    start = time.time() 
    for sensor in sens.sensors: 
        thread = threading.Thread(target = measure, args=(sensor,)) 
        threads.append(thread) 
        thread.start() 

    for thread in threads: 
        thread.join() 

    end = time.time() 
    print("\nTime taken:", end-start,"\n") 
    for key in data_saved: 
        for data in data_saved[key]:  
            print(f"{key.SENSOR}{key.index}: \n{json.dumps(data, indent=4)}\n") 
    return 0


if __name__ == '__main__':
    main()
