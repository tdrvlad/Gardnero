import logging, yaml, time
try:
    import RPi.GPIO as GPIO
    logging.info(*'Initialized RPi.GPIO library.')
except:
    import Mock.GPIO as GPIO
    logging.info(*'Initialized MOCK GPIO library.')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

seconds_in_day = 3600 * 24

with open(r'resources/gpio_map.yaml') as file:
    GPIO_MAP = yaml.safe_load(file)


def stop_gpio(gpio_pin):
    GPIO.output(gpio_pin, GPIO.HIGH)

def gpio_output_setup(gpio_pin):
    GPIO.setup(gpio_pin, GPIO.OUT)

def gpio_input_setup(gpio_pin):
    GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def execute_gpio(gpio_pin, exec_time):

    print('Executing GPIO pin {} for {} seconds.'.format(gpio_pin, exec_time))
    GPIO.output(GPIO_MAP.get('power'), GPIO.LOW)
    time.sleep(1)
    GPIO.output(gpio_pin, GPIO.LOW)
    time.sleep(exec_time)

    GPIO.output(gpio_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(GPIO_MAP.get('power'), GPIO.HIGH)
    time.sleep(2)
    print('Finished execution of GPIO pin {}.'.format(gpio_pin))

power_pin = GPIO_MAP.get('power')
if power_pin is None:
    print('Power Relay not found in wiring.')
else:
    gpio_output_setup(power_pin)
    stop_gpio(power_pin)
    

class Circuit:
    def __init__(self, pump, time, days_period, description=None):
        gpio_pin = GPIO_MAP.get(pump)
        if gpio_pin is None:
            print('Pump not found in wiring.')
        else:
            self.gpio_pin = gpio_pin
            gpio_output_setup(self.gpio_pin)
            stop_gpio(self.gpio_pin)
        self.time = time
        self.description = description
        self.days_period = days_period

        print('Created circuit for pump {} (GPIO {}).'.format(pump, self.gpio_pin))


class Circuits:
    def __init__(self, action_triggers):
        self.triggers = action_triggers.triggers

    def add_circuit(self, pump, time, days_period, description=None):
        circuit = Circuit(pump, time, days_period, description=None)

        for trigger in self.triggers:
            if trigger.days_period == circuit.days_period:
                trigger.add_circuit(circuit)


class ActionTrigger:
    def __init__(self, days_period):
        self.days_period = days_period
        self.period = self.days_period * seconds_in_day
        self.circuits = []
        self.timestamp = time.time()
        self.time_scale = 1

    def add_circuit(self, circuit):
        self.circuits.append(circuit)

    def tick(self):
        if time.time() > self.timestamp + self.period:
            print('Trigger {} days activated.'.format(self.days_period))
            self.activate()
        #print('Trigger {} days elapsed {:.1f} hours from last activation.'.format(self.days_period, (time.time() - self.timestamp)))


    def activate(self):
        self.timestamp = time.time()
        for circuit in self.circuits:
            if circuit.days_period == self.days_period:
                scaled_time = circuit.time * self.time_scale
                #try:
                execute_gpio(circuit.gpio_pin, scaled_time)
                #except:
                stop_gpio(circuit.gpio_pin)


class ActionTriggers:
    def __init__(self, max_days_period=4):
        self.triggers = []
        for i in range(1,max_days_period):
            self.triggers.append(ActionTrigger(days_period = i))

    def activate_all(self):
        for trigger in self.triggers:
            trigger.activate()

    def tick(self):
        for trigger in self.triggers:
            trigger.tick()
        

class Button:

    def __init__(self, action_triggers, handler):
        
        gpio_pin = GPIO_MAP.get('button_in')
        if gpio_pin is None:
            print('Button not found in wiring.')
        else:
            self.gpio_pin = gpio_pin
            gpio_input_setup(self.gpio_pin)
       
        self.handler = handler
        self.action_triggers = action_triggers


    
    def check_button(self):

        button = GPIO.input(self.gpio_pin)

        if button == GPIO.HIGH:
            print('Pressed button')
            start_time = time.time()
            time.sleep(0.5)
            while True:
                button = GPIO.input(self.gpio_pin)
                if button == GPIO.HIGH: 
                    self.handler.leds.turn_on_all() 
                    time.sleep(1)
                    self.handler.leds.turn_off_all() 
                    time.sleep(1)
                else:
                    break
            
                if time.time() - start_time > 6:
                    self.start_irigation()
                    break

            if time.time() - start_time > 2:
                self.change_mode()

    def change_mode(self):
        self.handler.change_mode()

    def start_irigation(self):
        self.action_triggers.activate_all()


class LEDs:

    def __init__(self, handler):
        led1_pin = GPIO_MAP.get('led1')
        led2_pin = GPIO_MAP.get('led2')
        led3_pin = GPIO_MAP.get('led3')

        if led1_pin is None or led2_pin is None or led3_pin is None:
            print('LEDs wiring not found.')
        
        else:
            self.led_pins = [led1_pin, led2_pin, led3_pin]

        for led_pin in self.led_pins:
            GPIO.setup(led_pin, GPIO.OUT)
        
        self.leds_on = False

        self.handler = handler

    def turn_on_led(self, led_no):
        GPIO.output(self.led_pins[led_no], GPIO.HIGH)

    def turn_off_led(self, led_no):
        GPIO.output(self.led_pins[led_no], GPIO.LOW)

    def turn_off_all(self):
        for led in range(len(self.led_pins)):
                self.turn_off_led(led)
        self.leds_on = False

    def turn_on_all(self):
        for led in range(len(self.led_pins)):
                self.turn_on_led(led)
        self.leds_on = True

    def blink(self):

        if self.leds_on is True:
            for led in range(len(self.led_pins)):
                self.turn_off_led(led)
            self.leds_on = False
        else:
            self.turn_on_led(self.handler.mode-1)
            self.leds_on = True
        

class Handler:

    def __init__(self, action_triggers, cycle_time = 2):
        self.mode = 2
        self.action_triggers = action_triggers
        self.cycle_time = cycle_time

        self.leds = LEDs(
            handler = self
        )
        self.button = Button(
            action_triggers = self.action_triggers, 
            handler = self)

    def change_mode(self):

        self.mode += 1
        if self.mode > 3:
            self.mode = 1

        print('Changed mode to {}'.format(self.mode))
        self.leds.turn_on_all()

        for action_trigger in self.action_triggers.triggers:
            action_trigger.time_scale = ((self.mode - 1) * (1.3 - 0.7)) / (3-1) + 0.7

    def run(self):
        while True:
            print('Mode: {}'.format(self.mode)) 
            self.action_triggers.tick()
            self.leds.blink()
            self.button.check_button()
            time.sleep(self.cycle_time)

 