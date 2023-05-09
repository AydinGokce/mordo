import board
import serial
import busio
import adafruit_pca9685
import numpy as np
import time
import traceback

from utils import get_servokit
from body_controller import BodyController


def format_sig_figs(value, max_digits):
    formatted_value = f"{value:.{max_digits}f}"
    return formatted_value


def normalize_angle(angle):
    normalized_angle = angle % 360.0

    return normalized_angle


def main2():
	kit1, kit2 = get_servokit()
	body = BodyController(kit1, kit2)
	

def main():

    time.sleep(1)
    moving_average_len = 5
    window = np.array([[0, 0]])

    kit1, kit2 = get_servokit()
    body = BodyController((kit1, kit2))
    
    uart_port = "/dev/serial0"  # This is the default UART port for Raspberry Pi
    uart_baudrate = 9600        # Set your desired baud rate
    uart = serial.Serial(uart_port, uart_baudrate, timeout=1)
    
    init_yaw, init_pitch = None, None
    
    
    for _ in range(5):
        data = uart.readline().decode("utf-8").strip()
    
    
    while True:
        try:
            data = uart.readline().decode("utf-8").strip()
            
            if init_pitch is None or init_yaw is None:
                init_yaw = normalize_angle(float(data.split("\t")[0].split(':')[-1]))
                init_pitch = normalize_angle(float(data.split("\t")[-1].split(':')[-1]))
                
            dx = normalize_angle(float(data.split("\t")[0].split(':')[-1]))
            dz = normalize_angle(float(data.split("\t")[-1].split(':')[-1]))
            
            dx_shifted = (180 - normalize_angle(dx + 180 - init_yaw)) * 0.5 * 1.5
            dz_shifted = (normalize_angle(dz + 180 - init_pitch) - 180) * 0.5 * 1.5
                                    
            #window = np.append(window, np.array([0, 0]), axis=1)
            #if window.shape[0] > moving_average_len:
            #    window = np.delete(window, -1, axis=1)
            #print(f"dx: {format_sig_figs(dx_shifted, 6)}, dx_raw: {dx}, init: {format_sig_figs(init_yaw, 6)}, yaw: {format_sig_figs(dx_shifted - 180,6)}")
            
            print(f"dx: {format_sig_figs(dx_shifted, 2)}, dx: {format_sig_figs(dx_shifted, 2)}")
            
            #body.angle_offset_head_yaw(dx_shifted*2)
            #body.angle_offset_head_pitch(dz_shifted * 1.4)
            
            #print(data)
            time.sleep(1/960)
    
        except KeyboardInterrupt:
            return
        except Exception as e:
            traceback.print_exc()


if __name__ == "__main__":
    main()
