import subprocess
import threading
import glob
import time
import board
import busio
import digitalio
import adafruit_ssd1306

from board import SCL, SDA
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, redirect, url_for, render_template, request

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


def scan_i2c():
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


def check_i2c_devices(I2C_DEVICE_LIST):
    DEVICE_ADDRS = {
        "OLED": "0x3c"
        # "Power Monitor": ""
    }
    for I2C_DEVICE in I2C_DEVICE_LIST:
        if I2C_DEVICE == "0x3c":
            print("OLED found!")
            OLED_FOUND = True
        time.sleep(2)             
        # if I2C_DEVICE == "":
        #     print(" found")
        #     _FOUND = True 


def test_leds(self):
    print("Testing LEDs...")
    time.sleep(1)
    self.green_led.value = self.LED_ON
    time.sleep(0.5)
    self.green_led.value = self.LED_OFF
    time.sleep(0.5)
    self.amber_led.value = self.LED_ON 
    time.sleep(0.5)
    self.amber_led.value = self.LED_OFF
    time.sleep(0.5)
    self.red_led.value = self.LED_ON
    time.sleep(0.5)
    self.red_led.value = self.LED_OFF
    print("LED Testing Complete")


def test_buzzer(self):
    print("Testing Buzzer...")
    time.sleep(1)
    self.buzzer.value = self.BUZZER_ON 
    time.sleep(0.5)
    self.buzzer.value = self.BUZZER_OFF
    print("Buzzer Test Complete")


def test_relays(self):
    print("Testing Water Pump...")
    time.sleep(1)
    self.water_pump.value = self.RELAY_PUMP_ON
    time.sleep(1)
    self.water_pump.value = self.RELAY_PUMP_OFF
    print("Water Pump Test Complete")

def test_ultra_sensor(self):
    print("Getting Water Level...")
    time.sleep(1)
    self.ultra_sonic_trig.value = self.ULTRA_SONIC_SENSOR_TRIGGER_ON
    time.sleep(0.00001)
    self.ultra_sonic_trig.value = self.ULTRA_SONIC_SENSOR_TRIGGER_OFF
    pulse_start = time.time()
    while self.ultra_sonic_echo.value == 0:
        pulse_start = time.time()
    
    pulse_stop = time.time()
    while self.ultra_sonic_echo.value == 1:
        pulse_stop = time.time()

    pulse_time = pulse_stop - pulse_start

    distance = (133 - int(pulse_time * 170000)) # sets distance to mm; speed = 2d/time
    print("Current Water Level:", distance, "mm")
    return distance


def test_temp_sensor():
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
    
def display_init(self, i2c = busio.I2C(SCL, SDA)):
    self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)


def display_setup(self):
    self.display.fill(0)
    self.display.show()
    width = self.display.width
    height = self.display.height
    self.image = Image.new("1", (width, height))
    self.draw = ImageDraw.Draw(self.image)
    self.draw.rectangle((0, 0, width, height), outline=0, fill=0)
    self.padding = -2
    self.top = self.padding
    self.bottom = height - self.padding
    self.x = 0
    self.font = ImageFont.load_default()


def display_stats(self):
    # Draw a black filled box to clear the image.
    self.draw.rectangle((0, 0, self.display.width, self.display.height),
        outline=0, fill=0)

    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'cut -f 1 -d " " /proc/loadavg'
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2}'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text
    self.draw.text((self.x, self.top + 0), "IP: " + IP, font=self.font, 
    fill=255)
    self.draw.text((self.x, self.top + 8), "CPU load: " + CPU, 
    font=self.font, fill=255)
    self.draw.text((self.x, self.top + 16), MemUsage, font=self.font, 
    fill=255)
    self.draw.text((self.x, self.top + 25), Disk, font=self.font, 
    fill=255)

    # Display image.
    self.display.image(self.image)
    self.display.show()


def display_measurements(self, distance, temp_celcius):
    self.draw.rectangle((0, 0, self.display.width, self.display.height),
        outline=0, fill=0)
    self.draw.text((self.x, self.top + 0), "Measurements:", 
    font=self.font, fill=255)
    self.draw.text((self.x, self.top + 16), "Water Level: " + str(distance) + "mm", 
    font=self.font, 
    fill=255)
    self.draw.text((self.x, self.top + 25), "Water Temp: " + str(temp_celcius) + " C", 
    font=self.font, fill=255)
    self.display.image(self.image)
    self.display.show()

 
def setup_temp_sensor(self):
    base_dir = '/sys/bus/w1/devices/'
    self.device_folder = glob.glob(base_dir + '28*')[0]
    self.device_file = self.device_folder + '/w1_slave'


def read_rom(self):
    name_file = self.device_folder + '/name'
    f = open(name_file,'r')
    return f.readline()


def read_temp_raw(self):
    f = open(self.device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(self):
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


def output_temp(temp_celcius):
    print('Water Temp: %3.3s C' % temp_celcius)

   
def read_sensor(self) -> int:
    self.ultra_sonic_trig.value = self.ULTRA_SONIC_SENSOR_TRIGGER_ON
    time.sleep(0.00001)
    self.ultra_sonic_trig.value = self.ULTRA_SONIC_SENSOR_TRIGGER_OFF
    pulse_start = time.time()
    
    while self.ultra_sonic_echo.value == 0:
        if time.time() - pulse_start >3:
            return None

    pulse_stop = time.time()

    pulse_time = pulse_stop - pulse_start

    distance = (133 - int(pulse_time * 170000)) # sonic speed = 343000 sets distance to mm; speed = 2d/time
    return distance


def maintain_water_level(self, distance):
    try:
        if distance is None:
            print("ERROR: Invalid Water Level Measurement")
            return
        # print("Water LeveL: ", distance, "mm")

        if distance in range(20,100): # to fill more than low range, change to lower value
            print("Water Level Nominal:", distance,"mm")
            self.green_led.value = self.LED_OFF
            self.amber_led.value = self.LED_ON
            self.red_led.value = self.LED_OFF
            self.buzzer.value = self.BUZZER_OFF
            self.water_pump.value = self.RELAY_PUMP_OFF
        elif distance < 20:
            print("Water level low:", distance,"mm")
            self.red_led.value = self.LED_ON
            self.green_led.value = self.LED_OFF
            self.amber_led.value = self.LED_OFF
            self.water_pump.value = self.RELAY_PUMP_ON
            self.buzzer.value = self.BUZZER_ON
            time.sleep(1)
            self.buzzer.value = self.BUZZER_OFF
        elif distance > 100: # would need to link to nominal lower range
            print("Water level full:", distance,"mm")
            self.amber_led.value = self.LED_OFF
            self.green_led.value = self.LED_ON
            self.red_led.value = self.LED_OFF
            self.water_pump.value = self.RELAY_PUMP_OFF
            self.buzzer.value = self.BUZZER_OFF

            time.sleep(1)

    except KeyboardInterrupt:
        print("Cleaning up...!")
        self.setup_GPIO()       

def main(self):
    __init__(self)
    setup_GPIO(self)
    I2C_DEVICE_LIST = scan_i2c()
    check_i2c_devices(I2C_DEVICE_LIST)

    print("\nInitialising RPi GPIO...")
    test_leds(self)
    test_buzzer(self)
    test_relays(self)
    test_ultra_sensor(self)
    test_temp_sensor()

    print("Setting up OLED Display...")
    display_init()
    display_setup()
    print("OLED Ready")
    display_stats()

    setup_temp_sensor()
    read_rom()

    print("Initialisation Complete!")
    print("\nStarting Measurements...")

    def background_reading():
        while True:
            distance = read_sensor()
            maintain_water_level()
            read_temp_raw()
            temp_celcius = read_temp()
            output_temp(temp_celcius)
            display_measurements(distance, temp_celcius)
            # time.sleep(3)

    background_thread = threading.Thread(target=background_reading, daemon=True)
    background_thread.start()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/home")
def homepage(distance):
    return render_template("home.html", distance=distance)
    

@app.route('/shutdown', methods=['POST', 'GET'])
def shutdown():
    return render_template("shutdown.html")


@app.route('/confirmshutdown', methods=['POST'])
def confirmshutdown():
    """Form submission confirmation from shutdown page."""
    shutdown_type = request.form.get('shutdownType')
    if shutdown_type == 'shutdown':
        subprocess.run('sudo shutdown -h 1', shell=True)
    elif shutdown_type == 'reboot':
        subprocess.run('sudo reboot -h 1 ', shell=True)
    else:
        return redirect(url_for('home'))
    return redirect(url_for('shutdown'))


@app.route("/metrics")
def metrics():
    return render_template("metrics.html")


@app.route("/logs")
def logs():
    return render_template("logs.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    main()
