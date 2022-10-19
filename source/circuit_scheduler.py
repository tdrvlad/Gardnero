from event_scheduler import EventScheduler
import time
from resources.parameters import CONFIG_FILE
import logging
import os
import yaml
from source.electrical_gpio import GPIOHandler

SECONDS_IN_DAY = 24 * 3600
SECONDS_IN_DAY = 1


class CircuitScheduler():
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.read_config()

        self.gpio_handler = GPIOHandler()
        self.event_scheduler = EventScheduler()
        self.event_scheduler.start()

        self.events = {}
        self.setup_events()
        self.add_led_blink_event()

    def add_led_blink_event(self):
        self.event_scheduler.enter_recurring(
            interval=5,
            priority=0,
            action=self.gpio_handler.blink_led,
            arguments=(
                self.config['mode'],
            )
        )

    def add_event(self, circuit_name):
        assert circuit_name in self.config['circuits'], f'Circuit {circuit_name} does not exist.'
        if circuit_name in self.events:
            event_id = self.events[circuit_name]
            self.event_scheduler.cancel_recurring(event_id)
        circuit_config = self.config['circuits'][circuit_name]
        event_id = self.event_scheduler.enter_recurring(
            interval=circuit_config['time_period_days'] * SECONDS_IN_DAY,
            priority=1,
            action=self.gpio_handler.run_pump,
            arguments=(
                circuit_config['pump_id'],
                circuit_config['time_duration_seconds'],
            )
        )
        self.events[circuit_name] = event_id


    def setup_events(self):
        for circuit_name in self.config['circuits'].keys():
            self.add_event(circuit_name)


    def add_circuit(self, circuit_name:str, pump_id:int, time_period_days:int, time_duration_seconds:int):
        if circuit_name in self.config['circuits']:
            return f'Circuit {circuit_name} already exists.'
        else:
            circuit_config = dict({})
            circuit_config['pump_id'] = pump_id
            circuit_config['time_period_days'] = time_period_days
            circuit_config['time_duration_seconds'] = time_duration_seconds
            self.config['circuits'][circuit_name] = circuit_config
            self.save_config()

            self.add_event(circuit_name)
            return self.config['circuits'][circuit_name]


    def change_circuit(self, circuit_name:str, time_period_days:int=0, time_duration_seconds:int=0):
        if circuit_name not in self.config['circuits']:
            return f'Circuit {circuit_name} does not exist.'
        else:
            if time_period_days:
                self.config['circuits'][circuit_name]['time_period_days'] = time_period_days
            if time_duration_seconds:
                self.config['circuits'][circuit_name]['time_duration_seconds'] = time_duration_seconds
            self.add_event(circuit_name)
            return self.config['circuits'][circuit_name]


    def read_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {'mode': 2, 'circuits': {}}
        return self.config


    def save_config(self):
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f)

    def get_circuits(self):
        return self.config['circuits']

    def get_circuit(self, circuit_name):
        if circuit_name in self.config['circuits']:
            return self.config['circuits'][circuit_name]
        else:
            return f'Circuit {circuit_name} does not exist.'

    def change_mode(self, mode):
        assert mode in [1, 2, 3]
        self.config['mode'] = mode
        self.save_config()

    def get_mode(self):
        return self.config['mode']

    def start_circuit(self, circuit_name, time_duration_seconds):
        assert circuit_name in self.config['circuits'], f'Circuit {circuit_name} does not exist.'
        circuit_config = self.config['circuits'][circuit_name]
        self.event_scheduler.enter(
            delay=1,
            priority=0,
            action=self.gpio_handler.run_pump,
            arguments=(
                circuit_config['pump_id'],
                time_duration_seconds,
            )
        )

    def start_pump(self, pump_id, time_duration_seconds):
        self.event_scheduler.enter(
            delay=1,
            priority=0,
            action=self.gpio_handler.run_pump,
            arguments=(
                pump_id,
                time_duration_seconds,
            )
        )

if __name__ == '__main__':
    circuit_scheduler = CircuitScheduler()
    for _ in range(10):
        print(circuit_scheduler.event_scheduler._lock)
    time.sleep(10)
    print('Changing.')
    circuit_scheduler.change_circuit('test_1', time_period_days=5)



