import time

import board
import digitalio


# defining variables for RPi 
ULTRA_SONIC_SENSOR_TRIGGER_PIN = board.D5 # BCM 29 = GPIO 5
ULTRA_SONIC_SENSOR_ECHO_PIN  = board.D6 # BCM 31 = GPIO 6
ULTRA_SONIC_SENSOR_TRIGGER_ON = True # ultra sonic sensor initiates reading
ULTRA_SONIC_SENSOR_TRIGGER_OFF = False 
ULTRA_SONIC_SENSOR_ECHO_ON = True # ultra sonic sensor returns reading
ULTRA_SONIC_SENSOR_ECHO_OFF = False

ultra_sonic_trig = digitalio.DigitalInOut(ULTRA_SONIC_SENSOR_TRIGGER_PIN)
ultra_sonic_echo = digitalio.DigitalInOut(ULTRA_SONIC_SENSOR_ECHO_PIN)
ultra_sonic_trig.direction = digitalio.Direction.OUTPUT
ultra_sonic_echo.direction = digitalio.Direction.INPUT
ultra_sonic_echo.pull = digitalio.Pull.DOWN

ultra_sonic_trig.value = ULTRA_SONIC_SENSOR_TRIGGER_ON
time.sleep(0.00001)
ultra_sonic_trig.value = ULTRA_SONIC_SENSOR_TRIGGER_OFF

def ultrasonic_test():      
    while True:
        pulse_start = 0
        pulse_stop = 0
        while ultra_sonic_echo.value == 0:
            pulse_start = time.time()

        while ultra_sonic_echo.value == 1:
            pulse_stop = time.time()

        pulse_time = pulse_stop - pulse_start

        distance = int(pulse_time * 170000) # sets distance to mm; speed = 2d/time
        print(distance)


def main():
   ultrasonic_test()

if __name__ == '__main__':
    main()