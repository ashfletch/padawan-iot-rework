'''
This application is to run a number of sensors to monitor the water level
within a closed loop system. The application can also detect when the water
level is critically low and pump water in to the main tank to tank to keep the
water level nominal. 
'''

import time
from initialize_pi import initialize
from oled import mini_oled
from sensors.water_level import water_level_sensor
from sensors.temperature import temperature_sensor


def main():
    myinit = initialize.Initializepi()
    myinit.setup_GPIO()
    I2C_DEVICE_LIST = myinit.scan_i2c()
    myinit.check_i2c_devices(I2C_DEVICE_LIST)

    mytestsensors = initialize.Testsensors()
    print("\nInitialising RPi GPIO...")
    mytestsensors.test_leds(myinit)
    mytestsensors.test_buzzer(myinit)
    mytestsensors.test_relays(myinit)
    mytestsensors.test_ultra_sensor(myinit)
    mytestsensors.test_temp_sensor()

    myoled = mini_oled.MiniOled()
    print("Setting up OLED Display...")
    myoled.display_init()
    myoled.display_setup()
    print("OLED Ready")
    myoled.display_stats()

    myultrasensor = water_level_sensor.Water_Level_Sensor()
    myultrasensor.setup_GPIO()

    mytempsensor = temperature_sensor.Temperature_Sensor()
    mytempsensor.setup_temp_sensor()
    mytempsensor.read_rom()

    print("Initialisation Complete!")
    print("\nStarting Measurements...")

    while True:
        distance = myultrasensor.read_sensor()
        myultrasensor.maintain_water_level()
        mytempsensor.read_temp_raw()
        temp_celcius = mytempsensor.read_temp()
        mytempsensor.output_temp(temp_celcius)
        myoled.display_measurements(distance, temp_celcius)
        time.sleep(3)


if __name__ == '__main__':
    main()
