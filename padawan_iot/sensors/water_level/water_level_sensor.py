import time
from os.path import exists

import board
import digitalio


class Water_Level_Sensor:

   def __init__(self) -> None:
      # defining variables for RPi
      self.ULTRA_SONIC_SENSOR_TRIGGER_PIN = board.D5 # BCM 29 = GPIO 5
      self.ULTRA_SONIC_SENSOR_ECHO_PIN  = board.D6 # BCM 31 = GPIO 6
      self.RED_LED_PIN = board.D23 # BCM 16 = GPIO 23
      self.AMBER_LED_PIN = board.D24 # BCM 18 = GPIO 24
      self.GREEN_LED_PIN = board.D18 # BCM 12 = GPIO 18
      self.BUZZER_PIN = board.D21 # BCM 40 = GPIO 21
      self.RELAY_WATER_PUMP_PIN = board.D16 # BCM 36 = GPIO 16
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
      # self.AVERAGING_INTERVAL = 1
      # self.NO_OF_SAMPLES = 10
      # self.WATER_LEVELS_FILE = '/home/pi/dev/padawan-iot-rework/padawan_iot/padawan_iot/water_level/water-level-data.csv'  


   def setup_GPIO(self) -> None:
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
      self.ultra_sonic_echo.pull = digitalio.Pull.DOWN

      self.red_led.value = self.LED_OFF
      self.amber_led.value = self.LED_OFF
      self.green_led.value = self.LED_OFF
      self.buzzer.value = self.BUZZER_OFF
      self.water_pump.value = self.RELAY_PUMP_OFF

   
   def read_sensor(self) -> int:
      pulse_start = 0
      pulse_stop = 0
      self.ultra_sonic_trig.value = self.ULTRA_SONIC_SENSOR_TRIGGER_ON
      time.sleep(0.0001)
      self.ultra_sonic_trig.value = self.ULTRA_SONIC_SENSOR_TRIGGER_OFF
      
      while self.ultra_sonic_echo.value == 0:
         pulse_start = time.time()

      while self.ultra_sonic_echo.value == 1:
         pulse_stop = time.time()

      pulse_time = pulse_stop - pulse_start

      distance = int(pulse_time * 170000) # sets distance to mm; speed = 2d/time
      return distance

   
   # def verify_read(self):
   #    dist = self.read_sensor()
   #    dist2 = self.read_sensor()
   #    dist3 = self.read_sensor()
   #    dist4 = self.read_sensor()
   #    dist5 = self.read_sensor()
   #    dist6 = self.read_sensor()
   #    dist7 = self.read_sensor()
   #    dist8 = self.read_sensor()
   #    dist9 = self.read_sensor()
   #    dist10 = self.read_sensor()
   #    water_level_average = ((dist + dist2 + dist3 + dist4 + dist5 + dist6 + dist7 + dist8 + dist9 + dist10) / 10)
   #    return water_level_average
      # water_level_measurements = []
      # while len(water_level_measurements) <= self.NO_OF_SAMPLES:
      # self.read_sensor()
      #    water_level_measurements.append(values)
      # sum = 0
      # for sample in water_level_measurements:
      #    sum += sample
      # water_level_average = int(sum / len(water_level_measurements))
      # print(water_level_average)


   # def verify_measurements(self):
   #    # lastGoodReading = -1
   #    water_level_data = []
   #    while len(water_level_data) <= self.NO_OF_SAMPLES:
   #       # verify_measurement(read_sensor(), lastGoodReading)
   #       test = self.read_sensor()
   #       print("test = ", test)
   #       water_level_data.append(test)
   #       # time.sleep(self.AVERAGING_INTERVAL/self.NO_OF_SAMPLES)
   #    sum = 0
   #    for sample in water_level_data:
   #       sum += sample
   #    water_level_average = int(sum / len(water_level_data))
   #    file_exists = exists(self.WATER_LEVELS_FILE)
   #    if file_exists:
   #       with open(self.WATER_LEVELS_FILE, 'a') as f:
   #          f.writelines(f'{water_level_average}\n')
   #       print("file found")
   #    else:
   #       print("file not found")
   #       with open(self.WATER_LEVELS_FILE, 'w') as f:
   #          f.writelines(f'{water_level_average}\n')
   #    with open(self.WATER_LEVELS_FILE, 'r') as f:
   #       lines = f.readlines()
   #       line = lines[-1].strip()
   #       water_level = line.split(',')
   #       print(water_level)


   def maintain_water_level(self):
      try:
         self.setup_GPIO()
         while True:
            distance = self.read_sensor()
            print(distance)

            if distance in range(50,100):
               print("Water Level Nominal")
               self.green_led.value = self.LED_ON
               self.amber_led.value = self.LED_OFF
               self.red_led.value = self.LED_OFF
               self.buzzer.value = self.BUZZER_OFF
               self.water_pump.value = self.RELAY_PUMP_OFF
            elif distance < 50:
               print("Water level is critically high")
               self.red_led.value = self.LED_ON
               self.green_led.value = self.LED_OFF
               self.amber_led.value = self.LED_OFF
               self.water_pump.value = self.RELAY_PUMP_ON
               self.buzzer.value = self.BUZZER_ON
               time.sleep(2)
               self.buzzer.value = self.BUZZER_OFF
            elif distance > 100:
               print("Water level is low")
               self.amber_led.value = self.LED_ON
               self.green_led.value = self.LED_OFF
               self.red_led.value = self.LED_OFF
               self.water_pump.value = self.RELAY_PUMP_OFF
               self.buzzer.value = self.BUZZER_ON
               time.sleep(2)
               self.buzzer.value = self.BUZZER_OFF

            time.sleep(1)

      except KeyboardInterrupt:
         print("Cleaning up...!")
         self.setup_GPIO()


def main():
   myultrasensor = Water_Level_Sensor()
   myultrasensor.setup_GPIO()
   print("Starting Measurements.....")
   time.sleep(0.1)
   myultrasensor.read_sensor()
   # myultrasensor.verify_measurements()
   # myultrasensor.verify_read()
   myultrasensor.maintain_water_level()
   

if __name__ == '__main__':
    main()
