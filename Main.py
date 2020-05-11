import RPi.GPIO as GPIO
import time
#----------------------------------

#defining irigation times (in seconds) according to specific plants
time_irigation1 = 10 #to be done daily
time_irigation2 = 35 #to be done once every 2 days
time_irigation3 = 17 #to be done once every 2 days
time_irigation4 = 7 #to be done once every 3 days

#----------------------------------

# GPIO MAP
# GPIO 2 - Relay 1 
# GPIO 20 - Relay 2 
# GPIO 4 - Relay 3
# GPIO 17 - Relay 4 
# GPIO 22 - Relay 5 
# GPIO 27 - Relay 6 
# GPIO 21 - Relay 7 
# GPIO 10 - Relay 8 - Power
# GPIO 9 - LED 1
# GPIO 11 - LED 2
# GPIO 6 - LED 3
# GPIO 26 - Button Input

relays = [None,2,20,4,17,22,27,21]
relay_power = 10
button_in = 26
leds = [None,9,11,6] 

#Setting up GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(relay_power,GPIO.OUT)
GPIO.output(relay_power,GPIO.HIGH)

for i in range(1,8):
	GPIO.setup(relays[i],GPIO.OUT)
	GPIO.output(relays[i],GPIO.HIGH)
	
for i in range(1,4):
	GPIO.setup(leds[i],GPIO.OUT)
	GPIO.output(leds[i],GPIO.LOW)

GPIO.setup(button_in,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#Setting up program
mode = 1
button_pressed = 0 

#defining tifferent timers: some irigation will be done daily, other once every 2 or 3 days 
timer_1day = time.time()
timer_2day = time.time()
timer_3day = time.time()
timer_leds = time.time()
timer_button = time.time()

trigger_1day = 0
trigger_2day = 0
trigger_3day = 0

seconds_in_hour = 3600
wait_time = 3 


def stop_all():
	GPIO.output(relay_power,GPIO.HIGH)
	for i in range(1,8):
		GPIO.output(relays[i],GPIO.HIGH)
	for i in range(1,4):
		GPIO.output(leds[i],GPIO.LOW)


def first_run():
	stop_all()
	for i in range(1,4):
		time.sleep(1)
		GPIO.output(leds[i],GPIO.HIGH)


def read_button():
	
	global button_pressed
	global mode

	global trigger_1day
	global trigger_2day
	global trigger_3day

	global timer_button

	button = GPIO.input(button_in)
	print 'Mode: ',mode
	print 'Button: ',button
	current_time = time.time()

	#Detecting button press
	#Short button press means changing the mode
	if button == GPIO.HIGH and button_pressed == 0:
		button_pressed = 1
		timer_button = current_time
		mode = (mode + 1) % 3
		#3 modes mean: half watering time, normal watering time and duble watering time
		print 'Button Pressed'
		print 'New mode: ',mode

	#Long button press means triggering all irigations
	if button == GPIO.HIGH and button_pressed == 1:
		if current_time - timer_button > 13:
			print 'Irigate Now Command'
			trigger_1day = 1
			mode = mode - 1
			if mode == 0:
				mode = 3
			trigger_2day = 1
			trigger_3day = 1

	if button == GPIO.LOW and button_pressed == 1:
		button_pressed = 0
	return mode


def leds_blink():

	global button_pressed
	global mode

	#Leds will blink to indicate normal running
	#Number of Leds will indicate the current mode

	if button_pressed == 1:
		for i in range(1,4):
			GPIO.output(leds[i],GPIO.HIGH)
	else:
		for i in range(1,4):
			GPIO.output(leds[i],GPIO.LOW)
		GPIO.output(leds[mode],GPIO.HIGH)
	
	time.sleep(wait_time)
	
	for i in range(1,4):
		GPIO.output(leds[i],GPIO.LOW)

	current_time = time.time()

	print 'Time to 1/1day watering: ',int(24 - (current_time - timer_1day)/seconds_in_hour),' hours'
	print 'Time to 1/2day watering: ',int(48 - (current_time - timer_2day)/seconds_in_hour),' hours'
	print 'Time to 1/3day watering: ',int(72 - (current_time - timer_3day)/seconds_in_hour),' hours'

	time.sleep(wait_time)


def check_time():

	global timer_1day
	global timer_2day
	global timer_3day
	global trigger_1day
	global trigger_2day
	global trigger_3day

	current_time = time.time()
	
	if current_time - timer_1day > 24 * seconds_in_hour:
		timer_1day = current_time
		trigger_1day = 1
		#print('1/1 day watering trigger')
	
	if current_time - timer_2day > 48 * seconds_in_hour:
		timer_2day = current_time
		trigger_2day = 1
		#print('1/2 days watering trigger')
	
	if current_time - timer_3day > 72 * seconds_in_hour:
		timer_3day = current_time
		trigger_3day = 1
		#print('1/3 days watering trigger')

	
def action(relay,timer):
	#Powering up the pumps
	GPIO.output(relay_power,GPIO.LOW) 
	time.sleep(1)
	
	#Setting the corresponding relay
	GPIO.output(relays[relay],GPIO.LOW)
	if(relay==5): #Iedera birou
		GPIO.output(relays[7],GPIO.LOW)
	
	#Keeping it active for preset time * mode (1,2 or 3) divided by 2 -> 0.5*time...1.5*time
	watering_time = int(timer*mode/2)
	time.sleep(watering_time)
	
	GPIO.output(relays[relay],GPIO.HIGH)
	GPIO.output(relays[7],GPIO.HIGH)
	
	#Powering down
	GPIO.output(relay_power,GPIO.HIGH)


def action_1day():

	global trigger_1day

	print 'Start watering 1/1 day'
	action(2,time_irigation1)
	trigger_1day = 0
	print 'Watering 1/1 day finished'


def action_2day():

	global trigger_2day

	print 'Start watering 1/2 days'
	action(20,time_irigation2)
	action(4,time_irigation3)
	trigger_2day = 0
	print 'Watering 1/2 days finished'


def action_3day():

	global trigger_3day

	print 'Start watering 1/3 days'
	action(17,time_irigation4)
	trigger_3day = 0
	print 'Watering 1/3 days finished'


first_run()

while 1:
	mode = read_button()
	leds_blink()
	check_time()
	
	if trigger_1day == 1:
		action_1day()
	if trigger_2day == 1:
		action_2day()
	if trigger_3day == 1:
		action_3day()
	if trigger_1day == 0 and trigger_2day == 0 and trigger_3day == 0:
		stop_all()





