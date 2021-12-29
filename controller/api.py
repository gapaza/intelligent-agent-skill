import os
import json
import time
import threading
import queue


# --> NXT Imports
import nxt.locator
from nxt.motor import *
from nxt.sensor.generic import Ultrasonic
from nxt.sensor.__init__ import Port as SPort


class Controller:
	def __init__(self, *args):
		self.queues = list(args)

	def stop(self):
		for q in self.queues:
			q.put_nowait({})


class NXTClient:
	
	
	def __init__(self):
		
		# --> 1. Init brick
		self.brick = nxt.locator.find()
		
		# --> 2. Init motors
		self.motor_a = self.brick.get_motor(Port.A)
		self.motor_b = self.brick.get_motor(Port.B)
		self.motor_c = self.brick.get_motor(Port.C)


		self.speeds = {
			'low': 15,
			'med': 45,
			'fast': 70,
			'full': 100,
		}
	
		# --> 3. Get sensors
		self.radar = Ultrasonic(self.brick, SPort.S4)

	def __str__(self):
		info = self.brick.get_device_info()
		return str(info)
	
	def get_charge(self):
		milli_volts = self.brick.get_battery_level()
		charge = str(milli_volts) + ' mV'
		return charge

	"""
		 __  __       _             
		|  \/  |     | |            
		| \  / | ___ | |_ ___  _ __ 
		| |\/| |/ _ \| __/ _ \| '__|
		| |  | | (_) | || (_) | |   
		|_|  |_|\___/ \__\___/|_|   
	"""

	@staticmethod
	def motor_run_state(motor):
		run_state = motor._get_state().run_state
		return run_state

	@staticmethod
	def run_motor(motor, power, wait=10):

		# --> 1. Define thread function
		def _run_motor(motor, power, queue, wait):
			# --> 1. Run motor
			motor.run(power=power, regulated=True)

			# --> 2. Check queue for stopping motor
			counter = 0
			sleep_counter = wait / 0.05
			while queue.empty():
				time.sleep(0.05)
				counter += 1
				if counter > sleep_counter:
					break

			# --> 3. Stop motor
			motor.idle()
			motor.brake()

		# --> 2. Create stop queue
		stop_queue = queue.Queue()

		# --> 3. Create thread + start
		th = threading.Thread(target=_run_motor, args=(motor, power, stop_queue, wait))
		th.start()

		# --> 4. Return stop queue
		return stop_queue

	@staticmethod
	def turn_motor(motor, speed, degrees, blocking=False):
		th = threading.Thread(target=motor.turn, args=(speed, degrees))
		th.start()
		if blocking is True:
			th.join()

	"""
		 __  __                
		|  \/  |               
		| \  / | _____   _____ 
		| |\/| |/ _ \ \ / / _ \
		| |  | | (_) \ V /  __/
		|_|  |_|\___/ \_/ \___|				
	"""

	def move(self, direction, power='low'):
		return self._move(direction, power)

	def _move(self, direction, power='low'):

		# --> 1. Get power from direction
		power = self.speeds[power]
		power_a = power
		power_b = power
		if direction == 'b':
			power_a *= -1
			power_b *= -1
		elif direction == 'cw':
			power_a *= -1
		elif direction == 'ccw':
			power_b *= -1

		# --> 2. Start motors
		a_stop_q = NXTClient.run_motor(self.motor_a, power_a)
		b_stop_q = NXTClient.run_motor(self.motor_b, power_b)

		# --> 3. Return controller
		return Controller(a_stop_q, b_stop_q)








	def move_forward_2(self, power='low', duration=1, force_break=True, blocking=False, reverse=False):
		
		power = int(self.speeds[power])
		if reverse is True:
			power *= -1
			
		commands = [
			threading.Thread(target=self.run_motor, args=('A', power, duration)),
			threading.Thread(target=self.run_motor, args=('B', power, duration))
		]
		
		for command in commands:
			command.start()
		
		if blocking is True:
			for command in commands:
				command.join()
		
		return
	
	def move_clockwise(self, power='low', duration=1, force_break=True, blocking=False, clockwise=True):
		
		a_power = int(self.speeds[power])
		b_power = int(self.speeds[power])
		
		if clockwise is False:
			b_power *= -1
		else:
			a_power *= -1
		
		commands = [
			threading.Thread(target=self.run_motor, args=('A', a_power, duration)),
			threading.Thread(target=self.run_motor, args=('B', b_power, duration))
		]
		
		for command in commands:
			command.start()
		
		if blocking is True:
			for command in commands:
				command.join()
		
		return

	"""
		 _____           _            
		|  __ \         | |           
		| |__) |__ _  __| | __ _ _ __ 
		|  _  // _` |/ _` |/ _` | '__|
		| | \ \ (_| | (_| | (_| | |   
		|_|  \_\__,_|\__,_|\__,_|_|   
	"""

	def rotate_radar(self, degrees, speed, clockwise=True, blocking=False):

		def convert_degrees(degrees_radar):
			degrees_motor = float(degrees_radar) / float(0.0666)
			return degrees_motor

		if clockwise is False:
			speed *= -1
		degrees = convert_degrees(degrees)
		NXTClient.turn_motor(self.motor_c, speed, degrees, blocking=blocking)

	def pulse_radar(self):
		return {
			'distance': float(self.radar.get_distance()),
			'units': str(self.radar.get_measurement_units())
		}





		
		
		
		
		
		
		



