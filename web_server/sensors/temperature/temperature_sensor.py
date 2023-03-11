import glob
import time

import board


class Temperature_Sensor:

    def __init__(self) -> None:
        # defining variables for RPi
        self.TEMPERATURE_SENS0R_PIN = board.D19 # BCM 35 = GPIO 19

    
    def setup_temp_sensor(self):
        base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

    
    def read_rom(self) -> str:
        name_file = self.device_folder + '/name'
        f = open(name_file,'r')
        return f.readline()


    def read_temp_raw(self) ->str:
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines


    def read_temp(self) -> int:
        lines = self.read_temp_raw()
        # Analyze if the last 3 characters are 'YES'.
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        # Find the index of 't=' in a string.
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            # Read the temperature .
            temp_string = lines[1][equals_pos+2:]
            temp_c = int(temp_string) / 1000.0
            temp_celcius = int(temp_c)
            return temp_celcius

        print(' rom: '+ self.read_rom())


    def output_temp(self, temp_celcius) -> None:
        print('Water Temp: %3.3s C' % temp_celcius)


def main():
   mytempsensor = Temperature_Sensor()
   mytempsensor.setup_temp_sensor()
   mytempsensor.read_rom()
   mytempsensor.read_temp_raw()
   temp_celcius = mytempsensor.read_temp()
   mytempsensor.output_temp(temp_celcius)

if __name__ == '__main__':
    main()
