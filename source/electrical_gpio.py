import yaml, time
from resources.parameters import GPIO_MAP_FILE

import logging, yaml, time
try:
    import RPi.GPIO as GPIO
    logging.info(*'Initialized RPi.GPIO library.')
except:
    import Mock.GPIO as GPIO
    logging.info(*'Initialized MOCK GPIO library.')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def stop_gpio(gpio_pin):
    GPIO.output(gpio_pin, GPIO.HIGH)

def gpio_output_setup(gpio_pin):
    GPIO.setup(gpio_pin, GPIO.OUT)

def gpio_input_setup(gpio_pin):
    GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def activate_gpio(gpio_pin):
    print(f'Activate pin {gpio_pin}')
    GPIO.output(gpio_pin, GPIO.LOW)

def deactivate_gpio(gpio_pin):
    print(f'Deactivate pin {gpio_pin}')
    GPIO.output(gpio_pin, GPIO.HIGH)


OUTPUTS = ['pump', 'led', 'power']

class GPIOHandler:
    def __init__(self, gpio_map_file=GPIO_MAP_FILE):
        self.gpio_map_file = gpio_map_file
        with open(self.gpio_map_file, 'r') as f:
            self.gpio_map = yaml.safe_load(f)
        self.setup()

    def setup(self):
        for name, pin in self.gpio_map.items():
            for o in OUTPUTS:
                if o in name:
                    gpio_output_setup(pin)

    def activate_pump(self, pump_id):
        activate_gpio(self.gpio_map['power'])
        time.sleep(0.5)
        activate_gpio(self.gpio_map[f'pump{pump_id}'])

    def deactivate_pump(self, pump_id):
        deactivate_gpio(self.gpio_map[f'pump{pump_id}'])
        time.sleep(0.5)
        activate_gpio(self.gpio_map['power'])

    def deqactivate_all(self):
        for name, pin in self.gpio_map.items():
            for o in OUTPUTS:
                if o in name:
                    deactivate_gpio(pin)

    def run_pump(self, pump_id, duration_seconds):
        print(f'Running pump {pump_id} for {duration_seconds} seconds.')
        self.activate_pump(pump_id)
        time.sleep(duration_seconds)
        self.deactivate_pump(pump_id)

    def blink_led(self, mode=2):
        assert mode in [1,2,3], f'Unknown led {mode}.'
        activate_gpio(self.gpio_map[f'led{mode}'])
        time.sleep(1)
        deactivate_gpio(self.gpio_map[f'led{mode}'])


def run_pump(pump_id, duration):
    print(f'Pump {pump_id} started.')
    time.sleep(duration)
    print(f'Pump {pump_id} stopped.')