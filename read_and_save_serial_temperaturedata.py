import serial
import csv
from datetime import datetime
import time
import os

# Setup serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust this to your Arduino's COM port

def get_filename():
    """Generate filename based on the current date."""
    today = datetime.now().strftime("%Y-%m-%d")
    return f'data/temperature_data_{today}.csv'

def write_header(writer, devices, file):
    """Write header to the CSV file based on the devices found."""
    headers = ['Time'] + [f"Temp{device}" for device in sorted(devices)]
    writer.writerow(headers)
    file.flush()  # Ensure header is immediately written to the file

def main():
    # Create 'data' directory if it does not exist
    if not os.path.exists('data'):
        os.makedirs('data')

    current_file = None
    writer = None
    file = None
    devices = set()
    last_readings = {}
    header_written = False

    try:
        while True:
            # Check if we need to switch files
            new_filename = get_filename()
            if new_filename != current_file:
                if file:
                    file.close()  # Close the old file if it was open
                file = open(new_filename, 'a', newline='')
                writer = csv.writer(file)
                current_file = new_filename

            line = ser.readline().decode('utf-8').strip()
            print(line) 
            
            # Process the line for device address or temperature
            if line.startswith("Device ") and "Address:" in line:
                # Parse the address of the device
                parts = line.split(':')
                device_hex = parts[1].strip()
                devices.add(device_hex)
            elif line == "<--":  # start of data packet
                last_readings = {} 
                timestamp = datetime.now().isoformat()  # take timestamp from start to save to the file
                if not header_written:
                    write_header(writer, devices, file)
                    header_written = True
            elif ',' in line:  # The line contains temperature readings
                device_hex, temperature = line.split(',')
                last_readings[device_hex] = temperature
            elif line == "-->":  # end of data packet - write line to file
                row = [timestamp] + [last_readings.get(device, "NaN") for device in sorted(devices)]
                writer.writerow(row)
                file.flush()  # Flush after every write to ensure data is saved immediately

    finally:
        if file:
            file.close()
        ser.close()

if __name__ == "__main__":
    main()