import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C bus
i2c = busio.I2C(SCL, SDA)

# Define I2C address of PCA9685
PCA9685_ADDRESS = 0x41

# Initialize PCA9685
pca = PCA9685(i2c, address=PCA9685_ADDRESS)
pca.frequency = 60

# Define target channel
CHANNEL = 15
time.sleep(20)
# Set duty cycle for the target channel to 100% (HIGH / 5V)
pca.channels[CHANNEL].duty_cycle = 0xFFFF



# Add a delay if you want to hold the HIGH signal for a specific duration
time.sleep(10)

# If you want to reset the channel after the delay, uncomment the following line
pca.channels[CHANNEL].duty_cycle = 0

# Clean up by deinitializing the PCA9685
pca.deinit()
