Code to read and save temperature from ds18b20 temperature sensors with Arduino and python

Arduino code is adapted from:
 * Rui Santos, https://randomnerdtutorials.com

See image here for wiring:
https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/07/ds18b20_arduino_multiple.png?w=1460&quality=100&strip=all&ssl=1

To run:  
1) Follow steps at https://randomnerdtutorials.com/guide-for-ds18b20-temperature-sensor-with-arduino/ to install OneWire and Dallas Temperature libraries in the Arduino IDE
2) Compile and upload code to the arduino.  Set the correct port if not connected at '/dev/ttyUSB0'.  The default wait time between measurements is 10 seconds - adjust this as needed
3) Install this package (pulls in pyserial):
```
pip install -e .
```
Note: do **not** run `pip install serial` — that is an unrelated, abandoned package. The correct dependency is `pyserial` (which is what `pip install -e .` installs), and it is imported in Python as `import serial`.

4) Run the python code to log data.  It will be saved as a .csv in the folder 'data':
```
python read_and_save_serial_temperaturedata.py
```

The python code starts a new csv file each day, and appends to current files so they can be viewed as the code is running.

## Running as a systemd service (Linux)

To run the logger as a long-lived background process that auto-restarts on crash and on boot, install it as a systemd unit.

1) Create the unit file at `/etc/systemd/system/bb-templogger.service`:

```ini
[Unit]
Description=BeesBook Temperature Logger
After=network.target

[Service]
Type=simple
User=beesbook
WorkingDirectory=/home/beesbook/bb2026/bb_temperatureloggers
ExecStart=/home/beesbook/anaconda3/envs/beesbook/bin/python read_and_save_serial_temperaturedata.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Adjust `User`, `WorkingDirectory`, and `ExecStart` to match your machine. **`ExecStart` must be the absolute path to the python interpreter inside your conda env** — find it by activating the env and running `which python`. systemd does not load your shell's PATH, so plain `python` will not work.

2) Enable and start the service:

```
sudo systemctl daemon-reload
sudo systemctl enable bb-templogger.service
sudo systemctl start bb-templogger.service
```

3) Check status and logs:

```
sudo systemctl status bb-templogger.service
sudo journalctl -u bb-templogger.service -f
```

### Gotchas

- **Serial port permissions**: if `/dev/ttyUSB0` is owned by group `dialout`, add the service user to that group so the script can open the port:
  ```
  sudo usermod -a -G dialout beesbook
  ```
  Reboot or log out/in for the group change to take effect.
- **Conda env python path**: point `ExecStart` directly at the env's python binary (e.g. `/home/beesbook/anaconda3/envs/beesbook/bin/python`). Do not try to `conda activate` from the unit file.
