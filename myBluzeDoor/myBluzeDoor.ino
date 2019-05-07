/*-------------------------
  Name:myBluzeDoor
  Author: SOUVAY Valentin
  Date: 22 mars 2019
  
--------------------------*/
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include "BlueDot_BME280.h"

const char* ssid = "Onilys";
const char* password = "w98kgi771";
const char* mqtt_server = "192.168.0.197";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsgbme = 0;
long lastMsgils = 0;
long lastMsgpir = 0;
char msg[50];
int value = 0;

BlueDot_BME280 bme1;                                     //Object for Sensor 1

int bme1Detected = 0;

const int pir = D5;
const int ils = D8;
void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println(); 
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is acive low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("home/state/door", "on");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void setup() {
  
   //Serial
   Serial.begin(115200);
   while (!Serial);
  /*Définition des pin
   * I2C-SDA  GPIO  5
   * I2C-SCK  GPIO  4
   * PIR      GPIO  15
   * ILS      GPIO  2
   * LED      GPIO  12
   * POTAR    A     0
   */
   
   //Pins
   Wire.begin(D1, D2);
   pinMode(pir, INPUT);
   pinMode(ils, INPUT);
   
 

  //Wifi
  setup_wifi();
  /*  
   *   WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);  
  WiFi.hostname("ESP_" door);
  WiFi.begin(ssid, password);
  digitalWrite(led,HIGH);
  while (WiFi.status() != WL_CONNECTED) 
  {
     delay(500);
     Serial.print("*");
  }  */   
  
  Serial.println("Connection done");
  
  //BME280
  
    bme1.parameter.I2CAddress = 0x76;
    bme1.parameter.sensorMode = 0b11;
    bme1.parameter.humidOversampling = 0b101;
    bme1.parameter.tempOversampling = 0b101;
    bme1.parameter.pressOversampling = 0b101;
    bme1.parameter.pressureSeaLevel = 1013.25;
    bme1.parameter.tempOutsideCelsius = 15;
    bme1.parameter.tempOutsideFahrenheit = 59;
     if (bme1.init() != 0x60)
  {    
    Serial.println(F("Ops!  BME280 Sensor not found!"));
    bme1Detected = 0;
  }

  else
  {
    Serial.println(F(" BME280 Sensor detected!"));
    bme1Detected = 1;
  }
  Serial.println(F("Bme ready"));
  //mqtt
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
   long now = millis();
   //Serial.println(now - lastMsgbme);
   if(bme1Detected && (now - lastMsgbme > 60000*10))  {
       lastMsgbme = now;
      sprintf(msg, "%ld", (int)bme1.readTempC());
      //Serial.println(msg);
      client.publish("home/temp/door" , msg);
      sprintf(msg, "%ld", (int)bme1.readPressure());
     // Serial.println(msg);
      client.publish("home/pressure/door" , msg);
      sprintf(msg, "%ld", (int)bme1.readHumidity());
      //Serial.println(msg);
      client.publish("home/humidity/door" , msg);
      Serial.println(" BME");
      
    }
    
    if(digitalRead(pir)==HIGH && (now - lastMsgpir > 10000))  {
    // Publish
      lastMsgpir = now;
      snprintf (msg, 75, "1");
      client.publish("home/pir/door" , msg);
      Serial.println(" pir");
        }
    if((digitalRead(ils)==HIGH)&& (now - lastMsgils > 10000)) {
      lastMsgils= now;
      snprintf (msg, 75, "1");
      client.publish("home/ils/door", msg);
      Serial.println("ils");
      
}

  
   
}
