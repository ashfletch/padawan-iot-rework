import time

import board
import digitalio


RELAY_WATER_PUMP_PIN = board.D16 # BCM 36 = GPIO 16
RELAY_PUMP_ON = False
RELAY_PUMP_OFF = True


water_pump = digitalio.DigitalInOut(RELAY_WATER_PUMP_PIN)
water_pump.direction = digitalio.Direction.OUTPUT
water_pump.value = RELAY_PUMP_OFF

def water_pump_test():
    water_pump.value = RELAY_PUMP_ON
    time.sleep(2)
    water_pump.value = RELAY_PUMP_OFF


def main():
    water_pump_test()

if __name__ == '__main__':
    main()
