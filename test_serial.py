import serial
import time

# Configure the UART connection
uart_port = "/dev/serial0"  # This is the default UART port for Raspberry Pi
uart_baudrate = 9600        # Set your desired baud rate

# Set up the UART connection
uart = serial.Serial(uart_port, uart_baudrate, timeout=1)

try:
    print("Reading UART data...")
    while True:
        # Read one line of data from the UART
        data = uart.readline().decode("utf-8").strip()

        # Check if there's any data
        if data:
            print("Data received: ", data)

        # Wait a bit before reading the next line of data
        time.sleep(1 / 9600)

except KeyboardInterrupt:
    print("\nExiting the program...")

finally:
    # Close the UART connection
    uart.close()
