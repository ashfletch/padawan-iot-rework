'''
This program takes an ultrasonic sensor measurement of the water level within
a container, and ouputs measurement to command line.
'''

import time

import board # import board library
import digitalio # import digitalio library


# defining variables for RPi 
ULTRA_SONIC_SENSOR_TRIGGER_PIN = board.D5 # BCM 29 = GPIO 5
ULTRA_SONIC_SENSOR_ECHO_PIN  = board.D6 # BCM 31 = GPIO 6
ULTRA_SONIC_SENSOR_TRIGGER_ON = True # assigning Boolean value to variable
ULTRA_SONIC_SENSOR_TRIGGER_OFF = False # assigning Boolean value to variable
ULTRA_SONIC_SENSOR_ECHO_ON = True # assigning Boolean value to variable
ULTRA_SONIC_SENSOR_ECHO_OFF = False # assigning Boolean value to variable

ultra_sonic_trig = digitalio.DigitalInOut(ULTRA_SONIC_SENSOR_TRIGGER_PIN) # define as I/O
ultra_sonic_echo = digitalio.DigitalInOut(ULTRA_SONIC_SENSOR_ECHO_PIN) # define as I/O
ultra_sonic_trig.direction = digitalio.Direction.OUTPUT # assign I/O direction as output
ultra_sonic_echo.direction = digitalio.Direction.INPUT # assign I/O direction as input
ultra_sonic_echo.pull = digitalio.Pull.DOWN # pull input value for retrieving measurements

ultra_sonic_trig.value = ULTRA_SONIC_SENSOR_TRIGGER_ON # set trig to Hi for 0.01ms
time.sleep(0.00001) 
ultra_sonic_trig.value = ULTRA_SONIC_SENSOR_TRIGGER_OFF # set trig to active Lo

def ultrasonic_test() -> int:   
    pulse_start = 0 # initialize start time
    pulse_stop = 0 # initialize stop time
    while ultra_sonic_echo.value == 0: # while no echo signal has been received, start pulse signal
        pulse_start = time.time()

    while ultra_sonic_echo.value == 1: # when echo signal has been received, stop pulse
        pulse_stop = time.time()

    pulse_time = pulse_stop - pulse_start # define time duration to use for distance equation below

    distance = (133 - int(pulse_time * 170000)) # time*sonic speed 343000/2 sets distance to mm; 
    print("Water level: ", distance, "mm")


def main() -> int:
   ultrasonic_test()

if __name__ == '__main__':
    main()