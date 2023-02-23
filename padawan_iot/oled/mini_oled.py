import time
import subprocess
import sys
import os

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

from sensors.water_level import water_level_sensor
from sensors.temperature import temperature_sensor

class MiniOled:

    def __init__(self) -> None:
        pass    

    
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
        self.draw.text((self.x, self.top + 0), "Water Level: " + distance, font=self.font, 
        fill=255)
        self.draw.text((self.x, self.top + 8), "Water Temp: " + temp_celcius, 
        font=self.font, fill=255)
        self.display.image(self.image)
        self.display.show()    


def main():
    myultrasensor = water_level_sensor.Water_Level_Sensor()
    mytempsensor = temperature_sensor.Temperature_Sensor()
    distance = myultrasensor.read_sensor()
    temp_celcius = mytempsensor.read_temp()
    myoled = MiniOled()
    myoled.display_init()
    myoled.display_setup()
    myoled.display_stats()
    myoled.display_measurements()


if __name__ == '__main__':
    main()
    