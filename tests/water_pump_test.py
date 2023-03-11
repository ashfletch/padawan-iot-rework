'''
This program performs a short test to power a water pump on and off.
'''

import time

import board
import digitalio

# define variables
RELAY_WATER_PUMP_PIN = board.D16 # BCM 36 = GPIO 16
RELAY_PUMP_ON = False # pump is active Hi by defualt, this inverts to Boolean
RELAY_PUMP_OFF = True # pump is active Hi by defualt, this inverts to Boolean

# define I/Os
water_pump = digitalio.DigitalInOut(RELAY_WATER_PUMP_PIN)
water_pump.direction = digitalio.Direction.OUTPUT

# initialise pump
water_pump.value = RELAY_PUMP_OFF

def water_pump_test() -> None:
    water_pump.value = RELAY_PUMP_ON
    time.sleep(2)
    water_pump.value = RELAY_PUMP_OFF


def main() -> None:
    water_pump_test()

if __name__ == '__main__':
    main()
