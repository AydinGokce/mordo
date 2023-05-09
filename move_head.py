import board
import serial
import busio
import adafruit_pca9685
import numpy as np
import time
import traceback
import keyboard
from utils import get_servokit
from body_controller import BodyController
	
kit1, kit2 = get_servokit()
body = BodyController((kit1, kit2))
    

"""def on_left_key(event):
    global body
    body.servos[6].add_angle(1)
    print("Left arrow key pressed")

def on_right_key(event):
    global body
    body.servos[6].add_angle(-1)
    print("Right arrow key pressed")

keyboard.on_press_key("left", on_left_key)
keyboard.on_press_key("right", on_right_key)

keyboard.wait()"""
sleep_factor = 0.015
angle = 60

for i in range(angle):
    body.servos[6].apply_angle(i)
    time.sleep(sleep_factor)

time.sleep(2)


for i in reversed(range(angle)):
    body.servos[6].apply_angle(i)
    time.sleep(sleep_factor)
    
    
for i in range(angle):
    body.servos[6].apply_angle(-i)
    time.sleep(sleep_factor)
time.sleep(2)

for i in reversed(range(angle)):
    body.servos[6].apply_angle(-i)
    time.sleep(sleep_factor)