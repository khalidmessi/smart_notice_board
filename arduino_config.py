import serial

# Serial connection settings
ARDUINO_PORT = '/dev/ttyUSB0'  # Replace with your actual port
BAUD_RATE = 9600

try:
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=0.05)
except serial.SerialException as e:
    print(f"Error: Could not open serial port {ARDUINO_PORT} - {e}")
    ser = None  # Ensure Flask doesn't crash if the port isn't available

def read_card():
    #Read RFID/NFC card data from Arduino.
    if ser and ser.in_waiting > 0:
        return ser.readline().decode('utf-8').strip()
    return None

"""import serial
import serial.tools.list_ports
import time

# Serial connection settings
ARDUINO_PORT = 'COM12'  # Replace with your actual port
BAUD_RATE = 9600

# Function to release the port if in use
def release_port(port):
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if p.device == port:
            try:
                ser = serial.Serial(port)
                ser.close()  # Close the port to release it
                print(f"Port {port} was in use and has been released.")
                time.sleep(1)  # Wait for the OS to free up the port
            except serial.SerialException:
                print(f"Could not release port {port}. It might be in use by another application.")

try:
    # Release the port if needed
    release_port(ARDUINO_PORT)
    
    # Open serial connection
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=0.05)
    print(f"Connected to {ARDUINO_PORT} successfully.")
except serial.SerialException as e:
    print(f"Error: Could not open serial port {ARDUINO_PORT} - {e}")
    ser = None  # Ensure the program doesn't crash

def read_card():
    #Read RFID/NFC card data from Arduino.
    if ser and ser.in_waiting > 0:
        return ser.readline().decode('utf-8').strip()
    return None
"""
