import time

import board
import digitalio

RED_LED_PIN = board.D23 # BCM 16 = GPIO 23
AMBER_LED_PIN = board.D24 # BCM 18 = GPIO 24
GREEN_LED_PIN = board.D18 # BCM 12 = GPIO 18
LED_ON = True
LED_OFF = False

red_led = digitalio.DigitalInOut(RED_LED_PIN)
amber_led = digitalio.DigitalInOut(AMBER_LED_PIN)
green_led = digitalio.DigitalInOut(GREEN_LED_PIN)

red_led.direction = digitalio.Direction.OUTPUT
amber_led.direction = digitalio.Direction.OUTPUT
green_led.direction = digitalio.Direction.OUTPUT

red_led.value = LED_OFF
amber_led.value = LED_OFF
green_led.value = LED_OFF

def led_test():
    green_led.value = LED_ON
    time.sleep(2)
    green_led.value = LED_OFF
    amber_led.value = LED_ON
    time.sleep(2)
    amber_led.value = LED_OFF
    red_led.value = LED_ON
    time.sleep(2)
    red_led.value = LED_OFF


def main():
   led_test()

if __name__ == '__main__':
    main()