/*
Adapted from:
 * Rui Santos, https://randomnerdtutorials.com
*/

#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

int numberOfDevices; // Number of temperature devices found
DeviceAddress tempDeviceAddress; // Store a found device address

// Variable to set wait time between measurements
unsigned int waitTime = 10000; // Default to 10000 milliseconds (10 seconds)

void setup(void) {
  Serial.begin(9600);
  sensors.begin();
  numberOfDevices = sensors.getDeviceCount();
  Serial.print("Found ");
  Serial.print(numberOfDevices, DEC);
  Serial.println(" devices.");
  for(int i = 0; i < numberOfDevices; i++) {
    if (sensors.getAddress(tempDeviceAddress, i)) {
      Serial.print("Device ");
      Serial.print(i);
      Serial.print(" Address: ");
      printAddress(tempDeviceAddress);
      Serial.println();
    } else {
      Serial.print("Found ghost device at ");
      Serial.print(i);
      Serial.println(" but could not detect address. Check power and cabling");
    }
  }
}

void loop(void) {
  sensors.requestTemperatures();
  Serial.println("<--");
  for(int i = 0; i < numberOfDevices; i++) {
    if(sensors.getAddress(tempDeviceAddress, i)){
      // Serial.print(i);
      printAddress(tempDeviceAddress);
      Serial.print(",");
      float tempC = sensors.getTempC(tempDeviceAddress);
      Serial.println(tempC);
    }  
  }
  Serial.println("-->");
  delay(waitTime);
}

void printAddress(DeviceAddress deviceAddress) {
  for (uint8_t i = 0; i < 8; i++) {
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}
