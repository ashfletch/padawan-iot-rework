'''
This program takes the continuous temperature within a liquid in both celcius
and farenheit, and outputs to command line.
'''

import os 
import glob
import time
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/' # define file path to devices dir
device_folder = glob.glob(base_dir + '28*')[0] # define folder name with "28" at index 0
device_file = device_folder + '/w1_slave' # file name

def read_temp_raw() -> str:
    f = open(device_file, 'r') # open device file in text mode
    lines = f.readlines() # read file
    f.close() # close file
    return lines # return the output of that file
 
def read_temp() -> float:
    lines = read_temp_raw() # assign output of read_temp_raw to variable lines
    while lines[0].strip()[-3:] != 'YES': # if YES is not found at tail of line
        time.sleep(0.2) # sleep
        lines = read_temp_raw() # re-read lines
    equals_pos = lines[1].find('t=') # find 't=' at start of line
    if equals_pos != -1: 
        temp_string = lines[1][equals_pos+2:] 
        temp_c = float(temp_string) / 1000.0 # temp_c = decimal
        temp_f = round(temp_c * 9.0 / 5.0 + 32.0,3) # convert celcius to farenheit
        return temp_c, temp_f # return both values
	
while True:
	print(read_temp())	
	time.sleep(1)