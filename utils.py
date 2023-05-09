import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit
from typing import Tuple, List
from servo import Servo
import os
import json

def get_servokit() -> Tuple[ServoKit, ServoKit]:
    # Set up the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Set up the PCA9685 servo breakout boards with different addresses
    pca1 = adafruit_pca9685.PCA9685(i2c, address=0x40)
    pca2 = adafruit_pca9685.PCA9685(i2c, address=0x41)

    # Set the PWM frequency to 50Hz (typical for servos)
    pca1.frequency = 50
    pca2.frequency = 50

    # Initialize two ServoKit instances for both PCA9685 boards
    kit1 = ServoKit(channels=16, i2c=i2c, address=0x40)
    kit2 = ServoKit(channels=16, i2c=i2c, address=0x41)
    
    return kit1, kit2


def get_servo_list(kits: Tuple[ServoKit, ServoKit]) -> List[Servo]:
    file_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_dir, "servo_setpoints.json"), "r") as f:
        servo_data = json.load(f)
    
    servos = []
    for servo in servo_data:
        servos.append(Servo.from_json(servo, kits))

    return servos