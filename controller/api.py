import os
import json
import time


# --> NXT Imports
import nxt.locator
from nxt.motor import *
from nxt.sensor.generic import Ultrasonic
from nxt.sensor.__init__ import Port as SPort

class NXTClient:


    def __init__(self):
        
        # --> 1. Locate nxt brick
        self.brick = nxt.locator.find()
       

        # --> 2. Get motors
        self.motor_a = self.brick.get_motor(Port.A)
        # self.motor_b = self.brick.get_motor(Port.B)
        # self.motor_c = self.brick.get_motor(Port.C)

        self.speeds = {
                'low': 20,
                'med': 45,
                'fast': 70,
                'full': 100,
        }

        
        # --> 3. Get sensors
        

        
        
    def __del__(self):
        self.brick.close()

    def __str__(self):
        info = self.brick.get_device_info()
        return str(info)
        
    def get_charge(self):
        milli_volts = self.brick.get_battery_level()
        return milli_volts

    def run_motor(self, motor='A', power='low', duration=1, force_break=True):
        
        if motor == 'A':
            motor = self.motor_a
        elif motor == 'B':
            motor = self.motor_b
        elif motor == 'C':
            motor = self.motor_c

        motor.run(power=self.speeds[power], regulated=True)
        time.sleep(duration) # Seconds
        motor.idle()

        if force_break is True:
            motor.brake()
            
    def get_distance(self):
        ultrasonic = Ultrasonic(self.brick, SPort.S1)
        distance = ultrasonic.get_distance()
        units = ultrasonic.get_measurement_units()
        return_str = str(distance) + ' ' + str(units)
        return return_str
		
		






        

    




















