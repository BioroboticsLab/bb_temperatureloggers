Code to read and save temperature from ds18b20 temperature sensors with Arduino and python

Arduino code is adapted from:
 * Rui Santos, https://randomnerdtutorials.com

See image here for wiring:
https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/07/ds18b20_arduino_multiple.png?w=1460&quality=100&strip=all&ssl=1

To run:  
1) Follow steps at https://randomnerdtutorials.com/guide-for-ds18b20-temperature-sensor-with-arduino/ to install OneWire and Dallas Temperature libraries in the Arduino IDE
2) Compile and upload code to the arduino.  Set the correct port if not connected at '/dev/ttyUSB0'.  The default wait time between measurements is 10 seconds - adjust this as needed
3) Install needed python libraries:
``` 
pip install pyserial
```
4) Run the python code to log data.  It will be saved as a .csv in the folder 'data':
```
python read_and_save_serial_temperaturedata.py
```

The python code starts a new csv file each day, and appends to current files so they can be viewed as the code is running.
