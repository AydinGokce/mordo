import board
import busio
import time
import adafruit_pca9685
from adafruit_servokit import ServoKit

# Set up the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Set up the PCA9685 servo breakout board
pca = adafruit_pca9685.PCA9685(i2c)
pca.frequency = 50  # Set the PWM frequency to 50Hz (typical for servos)

# Initialize the ServoKit library with 16 channels
kit = ServoKit(channels=16, i2c=i2c)

# Set the servo on channel 1 to 90 degrees
servo_channel = 12
servo_angle = 90
kit.servo[servo_channel].angle = servo_angle
time.sleep(0.5)
kit.servo[servo_channel].angle = 0
time.sleep(0.5)
kit.servo[servo_channel].angle = servo_angle



print(f"Servo on channel {servo_channel} set to {servo_angle} degrees")
