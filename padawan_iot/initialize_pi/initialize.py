import glob
import time

import board
import busio
import digitalio

class Initializepi:

    def __init__(self) -> None:
        # defining variables for RPi 
        self.RED_LED_PIN = board.D23 # BCM 16 = GPIO 23
        self.AMBER_LED_PIN = board.D24 # BCM 18 = GPIO 24
        self.GREEN_LED_PIN = board.D18 # BCM 12 = GPIO 18
        self.BUZZER_PIN = board.D21 # BCM 40 = GPIO 21
        self.RELAY_WATER_PUMP_PIN = board.D16 # BCM 36 = GPIO 16
        self.ULTRA_SONIC_SENSOR_TRIGGER_PIN = board.D5 # BCM 29 = GPIO 5
        self.ULTRA_SONIC_SENSOR_ECHO_PIN  = board.D6 # BCM 31 = GPIO 6
        self.TEMPERATURE_SENS0R_PIN = board.D19 # BCM 35 = GPIO 19
        self.RELAY_PUMP_ON = False
        self.RELAY_PUMP_OFF = True
        self.LED_ON = True
        self.LED_OFF = False
        self.BUZZER_ON = True
        self.BUZZER_OFF = False
        self.ULTRA_SONIC_SENSOR_TRIGGER_ON = True # ultra sonic sensor initiates reading
        self.ULTRA_SONIC_SENSOR_TRIGGER_OFF = False 
        self.ULTRA_SONIC_SENSOR_ECHO_ON = True # ultra sonic sensor returns reading
        self.ULTRA_SONIC_SENSOR_ECHO_OFF = False


    def setup_GPIO(self):
        self.red_led = digitalio.DigitalInOut(self.RED_LED_PIN)
        self.amber_led = digitalio.DigitalInOut(self.AMBER_LED_PIN)
        self.green_led = digitalio.DigitalInOut(self.GREEN_LED_PIN)
        self.buzzer = digitalio.DigitalInOut(self.BUZZER_PIN)
        self.water_pump = digitalio.DigitalInOut(self.RELAY_WATER_PUMP_PIN)
        self.ultra_sonic_trig = digitalio.DigitalInOut(self.ULTRA_SONIC_SENSOR_TRIGGER_PIN)
        self.ultra_sonic_echo = digitalio.DigitalInOut(self.ULTRA_SONIC_SENSOR_ECHO_PIN)

        self.red_led.direction = digitalio.Direction.OUTPUT
        self.amber_led.direction = digitalio.Direction.OUTPUT
        self.green_led.direction = digitalio.Direction.OUTPUT
        self.buzzer.direction = digitalio.Direction.OUTPUT
        self.water_pump.direction = digitalio.Direction.OUTPUT
        self.ultra_sonic_trig.direction = digitalio.Direction.OUTPUT
        self.ultra_sonic_echo.direction = digitalio.Direction.INPUT

        self.red_led.value = self.LED_OFF
        self.amber_led.value = self.LED_OFF
        self.green_led.value = self.LED_OFF
        self.buzzer.value = self.BUZZER_OFF
        self.water_pump.value = self.RELAY_PUMP_OFF


    def scan_i2c(self):
        I2C_DEVICE_LIST = []
        # Create the I2C interface.
        i2c = busio.I2C(board.SCL, board.SDA)
        try:
            for device_address in i2c.scan():
                print("Scanning I2C bus...")
                time.sleep(2)
                device_address = hex(device_address)
                # print("Device = ", device_address)
                I2C_DEVICE_LIST.append(device_address)
        except:
            print("No I2C address found")
        return I2C_DEVICE_LIST


    def check_i2c_devices(self, I2C_DEVICE_LIST):
        DEVICE_ADDRS = {
            "OLED": "0x3c"
            # "Power Monitor": ""
        }
        for I2C_DEVICE in I2C_DEVICE_LIST:
            if I2C_DEVICE == "0x3c":
                print("\nOLED found!")
                OLED_FOUND = True
            time.sleep(2)             
            # if I2C_DEVICE == "":
            #     print(" found")
            #     _FOUND = True 

class Testsensors:
    def __init__(self) -> None:
        # self.mytestinit = Initializepi()
        pass


    def test_leds(self, mytestinit):
        print("Testing LEDs...")
        time.sleep(1)
        mytestinit.green_led.value = mytestinit.LED_ON
        time.sleep(0.5)
        mytestinit.green_led.value = mytestinit.LED_OFF
        time.sleep(0.5)
        mytestinit.amber_led.value = mytestinit.LED_ON 
        time.sleep(0.5)
        mytestinit.amber_led.value = mytestinit.LED_OFF
        time.sleep(0.5)
        mytestinit.red_led.value = mytestinit.LED_ON
        time.sleep(0.5)
        mytestinit.red_led.value = mytestinit.LED_OFF
        print("LED Testing Complete")


    def test_buzzer(self, mytestinit):
        print("Testing Buzzer...")
        time.sleep(1)
        mytestinit.buzzer.value = mytestinit.BUZZER_ON 
        time.sleep(0.5)
        mytestinit.buzzer.value = mytestinit.BUZZER_OFF
        print("Buzzer Test Complete")
    
    
    def test_relays(self, mytestinit):
        print("Testing Water Pump...")
        time.sleep(1)
        mytestinit.water_pump.value = mytestinit.RELAY_PUMP_ON
        time.sleep(1)
        mytestinit.water_pump.value = mytestinit.RELAY_PUMP_OFF
        print("Water Pump Test Complete")

    def test_ultra_sensor(self, mytestinit):
        print("Getting Water Level...")
        time.sleep(1)
        mytestinit.ultra_sonic_trig.value = mytestinit.ULTRA_SONIC_SENSOR_TRIGGER_ON
        time.sleep(0.00001)
        mytestinit.ultra_sonic_trig.value = mytestinit.ULTRA_SONIC_SENSOR_TRIGGER_OFF
        pulse_start = time.time()
        while mytestinit.ultra_sonic_echo.value == 0:
            pulse_start = time.time()
        
        pulse_stop = time.time()
        while mytestinit.ultra_sonic_echo.value == 1:
            pulse_stop = time.time()

        pulse_time = pulse_stop - pulse_start

        distance = int(pulse_time * 170000) # sets distance to mm; speed = 2d/time
        print("Current Water Level:", distance, "mm")
        return distance

    
    def test_temp_sensor(self):
        print("Getting Water Temp...")
        time.sleep(1)
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        # Analyze if the last 3 characters are 'YES'.
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            f = open(device_file, 'r')
            lines = f.readlines()
            f.close()
        # Find the index of 't=' in a string.
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            # Read the temperature .
            temp_string = lines[1][equals_pos+2:]
            temp_c = int(temp_string) / 1000.0
            temp_celcius = int(temp_c)
            print("Current Water Temp:", temp_celcius, "C")
        return temp_celcius
        

def main():
    myinit = Initializepi()
    myinit.setup_GPIO()
    I2C_DEVICE_LIST = myinit.scan_i2c()
    myinit.check_i2c_devices(I2C_DEVICE_LIST)
    mytestsensors = Testsensors()
    mytestsensors.test_leds(myinit)
    mytestsensors.test_buzzer(myinit)
    mytestsensors.test_relays(myinit)
    mytestsensors.test_ultra_sensor(myinit)
    mytestsensors.test_temp_sensor()
    print('\nInitialisation Complete!')

if __name__ == '__main__':
    main()
