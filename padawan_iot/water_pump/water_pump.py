import time

import board
import digitalio


class Water_Pump():

    def __init__(self) -> None:
        # defining variables for RPi
        self.RELAY_WATER_PUMP_PIN = board.D16 # BCM 36 = GPIO 16
        self.RELAY_PUMP_ON = False
        self.RELAY_PUMP_OFF = True


    def setup_GPIO(self):
        self.water_pump = digitalio.DigitalInOut(self.RELAY_WATER_PUMP_PIN)
        self.water_pump.direction = digitalio.Direction.OUTPUT
        self.water_pump.value = self.RELAY_PUMP_OFF


    def control_pump(self):
        self.water_pump.value = self.RELAY_PUMP_ON
        time.sleep(1)
        self.water_pump.value = self.RELAY_PUMP_OFF


def main():
    mywaterpump = Water_Pump()
    mywaterpump.setup_GPIO()
    mywaterpump.control_pump()

if __name__ == '__main__':
    main()
