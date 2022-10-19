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

def gpio_output_setup(gpio_pin):
    GPIO.setup(gpio_pin, GPIO.OUT)

def gpio_input_setup(gpio_pin):
    GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def activate_relay(gpio_pin):
    GPIO.output(gpio_pin, GPIO.LOW)

def deactivate_relay(gpio_pin):
    GPIO.output(gpio_pin, GPIO.HIGH)

def activate_led(gpio_pin):
    GPIO.output(gpio_pin, GPIO.HIGH)

def deactivate_led(gpio_pin):
    GPIO.output(gpio_pin, GPIO.LOW)

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
                    if o == 'led':
                        deactivate_led(pin)
                    else:
                        deactivate_relay(pin)

    def activate_pump(self, pump_id):
        activate_relay(self.gpio_map['power'])
        time.sleep(0.5)
        activate_relay(self.gpio_map[f'pump{pump_id}'])

    def deactivate_pump(self, pump_id):
        deactivate_relay(self.gpio_map[f'pump{pump_id}'])
        time.sleep(0.5)
        activate_relay(self.gpio_map['power'])

    def deqactivate_all(self):
        for name, pin in self.gpio_map.items():
            for o in OUTPUTS:
                if o in name:
                    deactivate_relay(pin)

    def run_pump(self, pump_id, duration_seconds):
        print(f'Running pump {pump_id} for {duration_seconds} seconds.')
        self.activate_pump(pump_id)
        time.sleep(duration_seconds)
        self.deactivate_pump(pump_id)

    def blink_led(self, mode=2):
        assert mode in [1, 2, 3], f'Unknown led {mode}.'
        activate_led(self.gpio_map[f'led{mode}'])
        time.sleep(1)
        deactivate_led(self.gpio_map[f'led{mode}'])