import time

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


   def setup_GPIO(self) -> None:
      # define I/Os
      self.red_led = digitalio.DigitalInOut(self.RED_LED_PIN)
      self.amber_led = digitalio.DigitalInOut(self.AMBER_LED_PIN)
      self.green_led = digitalio.DigitalInOut(self.GREEN_LED_PIN)
      self.buzzer = digitalio.DigitalInOut(self.BUZZER_PIN)
      self.water_pump = digitalio.DigitalInOut(self.RELAY_WATER_PUMP_PIN)
      self.ultra_sonic_trig = digitalio.DigitalInOut(self.ULTRA_SONIC_SENSOR_TRIGGER_PIN)
      self.ultra_sonic_echo = digitalio.DigitalInOut(self.ULTRA_SONIC_SENSOR_ECHO_PIN)

      #define I/O directions
      self.red_led.direction = digitalio.Direction.OUTPUT
      self.amber_led.direction = digitalio.Direction.OUTPUT
      self.green_led.direction = digitalio.Direction.OUTPUT
      self.buzzer.direction = digitalio.Direction.OUTPUT
      self.water_pump.direction = digitalio.Direction.OUTPUT
      self.ultra_sonic_trig.direction = digitalio.Direction.OUTPUT
      self.ultra_sonic_echo.direction = digitalio.Direction.INPUT
      self.ultra_sonic_echo.pull = digitalio.Pull.DOWN

      # initialise devices
      self.red_led.value = self.LED_OFF
      self.amber_led.value = self.LED_OFF
      self.green_led.value = self.LED_OFF
      self.buzzer.value = self.BUZZER_OFF
      self.water_pump.value = self.RELAY_PUMP_OFF

   
   def read_sensor(self) -> int:
      time.sleep(1)
      self.ultra_sonic_trig.value = self.ULTRA_SONIC_SENSOR_TRIGGER_ON
      time.sleep(0.00001)
      self.ultra_sonic_trig.value = self.ULTRA_SONIC_SENSOR_TRIGGER_OFF
      pulse_start = time.time()
      while self.ultra_sonic_echo.value == 0:
         pulse_start = time.time()
         if time.time() - pulse_start >3:
            return None

      pulse_stop = time.time()
      while self.ultra_sonic_echo.value == 1:
         pulse_stop = time.time()

      pulse_time = pulse_stop - pulse_start

      distance = (133 - int(pulse_time * 170000)) # sonic speed = 343000 sets distance to mm; speed = 2d/time
      return distance


   def maintain_water_level(self) -> None:
      try:
         self.setup_GPIO()
         distance = self.read_sensor()
         if distance is None:
            print("ERROR: Invalid Water Level Measurement")
            return

         if distance in range(50,80): # to fill more than low range, change to lower value
            print("Water Level Nominal:", distance,"mm")
            self.green_led.value = self.LED_OFF
            self.amber_led.value = self.LED_ON
            self.red_led.value = self.LED_OFF
            self.buzzer.value = self.BUZZER_OFF
            self.water_pump.value = self.RELAY_PUMP_OFF
         elif distance < 50:
            print("Water level low:", distance,"mm")
            self.red_led.value = self.LED_ON
            self.green_led.value = self.LED_OFF
            self.amber_led.value = self.LED_OFF
            self.water_pump.value = self.RELAY_PUMP_ON
            self.buzzer.value = self.BUZZER_ON
            time.sleep(1)
            self.buzzer.value = self.BUZZER_OFF
            time.sleep(25)
            self.water_pump.value = self.RELAY_PUMP_OFF            
         elif distance > 80: # would need to link to nominal lower range
            print("Water level high", distance,"mm")
            self.amber_led.value = self.LED_OFF
            self.green_led.value = self.LED_ON
            self.red_led.value = self.LED_OFF
            self.water_pump.value = self.RELAY_PUMP_OFF
            self.buzzer.value = self.BUZZER_OFF

      except KeyboardInterrupt:
         print("Cleaning up...!")
         self.setup_GPIO()


# def main() -> None:
#    myultrasensor = Water_Level_Sensor()
#    myultrasensor.setup_GPIO()
#    print("Starting Measurements.....")
#    time.sleep(1)
#    myultrasensor.maintain_water_level()
   

# if __name__ == '__main__':
#     main()
