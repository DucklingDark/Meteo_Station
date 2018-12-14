#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>
#include <WString.h>
#include <Wire.h>
#include "math.h"
#include "..\include\protocol.h"
#include "..\include\Adafruit_Sensor.h"
#include "..\include\Adafruit_BMP085_U.h"
#include "..\include\HTU21D.h"
/***************************************************************************/
#define HPA_TO_MM       0.750062
/***************************************************************************/
const char* ssid        = "***";
const char* password    = "***";
/***************************************************************************/
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);
HTU21D  myHTU21D(HTU21D_RES_RH11_TEMP11);
/***************************************************************************/
WiFiServer  server(90);
String      header;
uint8_t     clientReady     = 0;
uint8_t     rxState         = 0;
String      rxMsg           = "";
String      txMsg           = "";
char        txChar[50];
uint8_t     i               = 0;
unsigned long lastMillis    = 0;
unsigned long currMillis    = 0;
float       bmpTemp         = 0.0;
float       htuTemp         = 0.0;
float       pressure        = 0.0;
float       humidity        = 0.0;
uint8_t     newData         = 0;
/***************************************************************************/
void setup() {
    Serial.begin(115200);
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected.");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    server.begin();

    myHTU21D.begin();
    bmp.begin();
}
/***************************************************************************/
void getBMP(){
    sensors_event_t event;
    bmp.getEvent(&event);

    if (event.pressure){
        pressure = event.pressure * HPA_TO_MM;
        Serial.print("Pressure:\t\t");
        Serial.print(pressure);
        Serial.println(" mm");

        bmp.getTemperature(&bmpTemp);
        Serial.print("BMP180 Temperature:\t");
        Serial.print(bmpTemp);
        Serial.println(" C");

        Serial.println();
    }
}
/***************************************************************************/
void getHTU(){
    humidity = myHTU21D.readHumidity();
    htuTemp = myHTU21D.readTemperature();
    Serial.print(F("Humidity:\t\t")); Serial.print(humidity); Serial.println(F(" +-2%"));
    Serial.print(F("Temperature:\t\t")); Serial.print(htuTemp); Serial.println(F(" +-0.3C"));
    Serial.println();
    myHTU21D.softReset();
    myHTU21D.setResolution(HTU21D_RES_RH11_TEMP11);
}
/***************************************************************************/
void loop() {
    WiFiClient client = server.available();

    if (client) {
        Serial.println("Client.");
        String currentLine = "";
        rxState = 0;

        while (client.connected()) {

            currMillis = millis();

            if (abs(currMillis - lastMillis) >= 100){
                getHTU();
                getBMP();
                newData = 1;
                lastMillis = millis();
            }

            if (client.available()) {
                char c = client.read();

                if (c == '$'){
                    rxMsg = "";
                } else {
                    if (c != '\n'){
                        rxMsg += c;
                    } else {
                        if (c == '\n') {
                            if (rxMsg == "OK"){
                                Serial.println(rxMsg);
                                clientReady = 1;
                            }
                        }
                    }
                }

                if (clientReady == 1 && newData == 1){
                    clientReady = 0;
                    newData = 0;
                    txMsg = prepareMessage((String)bmpTemp, TEMP_BPM_CMD);
                    txMsg.toCharArray(txChar, 50);
                    client.write(txChar);

                    txMsg = prepareMessage((String)htuTemp, TEMP_HTU_CMD);
                    txMsg.toCharArray(txChar, 50);
                    client.write(txChar);

                    txMsg = prepareMessage((String)pressure, PRESSURE_CMD);
                    txMsg.toCharArray(txChar, 50);
                    client.write(txChar);

                    txMsg = prepareMessage((String)humidity, HUMIDITY_CMD);
                    txMsg.toCharArray(txChar, 50);
                    client.write(txChar);
                    Serial.println("sended");
                }
            }
        }

        header = "";
        client.stop();
        Serial.println("Client disconnected.");
        Serial.println("");
    }
}
/***************************************************************************/
