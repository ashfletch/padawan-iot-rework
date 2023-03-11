'''
This program performs a short illumination test of connected LEDs.
'''

import time

import board
import digitalio

RED_LED_PIN = board.D23 # BCM 16 = GPIO 23
AMBER_LED_PIN = board.D24 # BCM 18 = GPIO 24
GREEN_LED_PIN = board.D18 # BCM 12 = GPIO 18
LED_ON = True # assigning Boolean value to variable
LED_OFF = False # assigning Boolean value to variable

# define as I/Os
red_led = digitalio.DigitalInOut(RED_LED_PIN) 
amber_led = digitalio.DigitalInOut(AMBER_LED_PIN) 
green_led = digitalio.DigitalInOut(GREEN_LED_PIN) 

# assign I/O direction as outputs
red_led.direction = digitalio.Direction.OUTPUT 
amber_led.direction = digitalio.Direction.OUTPUT 
green_led.direction = digitalio.Direction.OUTPUT 

# initialise LEDs to OFF
red_led.value = LED_OFF
amber_led.value = LED_OFF
green_led.value = LED_OFF

def led_test() -> None:
    green_led.value = LED_ON # turn green LED on for 2 seconds
    time.sleep(2)
    green_led.value = LED_OFF
    amber_led.value = LED_ON # turn amber LED on for 2 seconds
    time.sleep(2)
    amber_led.value = LED_OFF
    red_led.value = LED_ON # turn red LED on for 2 seconds
    time.sleep(2)
    red_led.value = LED_OFF


def main() -> None:
   led_test()

if __name__ == '__main__':
    main()