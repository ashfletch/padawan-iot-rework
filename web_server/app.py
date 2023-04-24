'''
This program is the main driver of the project, which performs an intialisation/
POST of connected devices to Raspberry Pi, as well as displaying the RPi system
statistics. The program itself has been written to measure the current water
level and water temperature within a water tank, and output these measurements
to a local OLED display, and downstream Flask GUI accessible via RPi WAP.
'''

import subprocess
import threading
import time

from flask import Flask, redirect, url_for, render_template, request
from web_server.initialize_pi import initialize
from web_server.oled import mini_oled
from web_server.sensors.water_level import water_level_sensor
from web_server.sensors.temperature import temperature_sensor

pi = initialize.Initializepi()
pi.setup_GPIO()
I2C_DEVICE_LIST = pi.scan_i2c()
pi.check_i2c_devices(I2C_DEVICE_LIST)

mytestsensors = initialize.Testsensors()
print("\nInitialising RPi GPIO...")
mytestsensors.test_leds(pi)
mytestsensors.test_buzzer(pi)
mytestsensors.test_relays(pi)
mytestsensors.test_ultra_sensor(pi)
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

def get_water_level() -> int:
    return myultrasensor.read_sensor()

def get_water_temp() -> int:
    return mytempsensor.read_temp()

def background_reading() -> None:
    while True:
        distance = myultrasensor.read_sensor()
        myultrasensor.maintain_water_level()
        mytempsensor.read_temp_raw()
        temp_celcius = mytempsensor.read_temp()
        mytempsensor.output_temp(temp_celcius)
        myoled.display_measurements(distance, temp_celcius)

background_thread = threading.Thread(target=background_reading, daemon=True)
background_thread.start()

app = Flask(__name__)

@app.route("/")
def home() -> str:
    distance = get_water_level()
    distance_percentage = (distance / 133) * 100 # 0.126 = 12.6 cm internal height of tank
    fill_line = distance_percentage * 2.25 # convert distance to pixels in tank graphic
    empty_fill_line = 225 - fill_line # empty line inverse of fill line
    temp = get_water_temp()
    return render_template("home.html", distance=distance, temp=temp, fill_line=fill_line, empty_fill_line=empty_fill_line)


@app.route("/home")
def homepage() -> str:
    return render_template("home.html")
    

@app.route('/shutdown', methods=['POST', 'GET'])
def shutdown() -> str:
    return render_template("shutdown.html")


@app.route('/shutdown/confirm', methods=['POST'])
def confirmshutdown():
    """Form submission confirmation from shutdown page."""
    shutdown_type = request.form.get('shutdownType')
    if shutdown_type == 'shutdown':
        subprocess.run('sudo shutdown -h 1', shell=True)
    elif shutdown_type == 'reboot':
        subprocess.run('sudo reboot -h 1 ', shell=True)
    else:
        return redirect(url_for('/'))
    return redirect(url_for('shutdown'))


@app.route("/metrics")
def metrics() -> str:
    return render_template("metrics.html")


@app.route("/logs")
def logs() -> str:
    return render_template("logs.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
