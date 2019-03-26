/*-------------------------
  Name:myBluzeDoor
  Author: SOUVAY Valentin
  Date: 22 mars 2019
  
--------------------------*/
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SoftwareSerial.h>

const char* ssid = "Livebox-AC10";
const char* password = "yvzcH9voyY3eV7PrCv";
const char* mqtt_server = "192.168.1.45";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsgsmk = 0;
long lastMsgpir = 0;
char msg[50];
int value = 0;
long now;

const int smk = A0;
const int pir = D1;

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
      client.publish("home/state/smoke", "on");
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
     
   //Pins
   pinMode(smk, INPUT);
   pinMode(pir, INPUT);

  //Wifi
  setup_wifi();
  
  
  Serial.println("Connection done");
  
    
  Serial.println(F("Smk ready"));
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
   now = millis();
      
    if(analogRead(smk)>400 && (now - lastMsgsmk > 100))  {
    // Publish
      lastMsgsmk = now;
      snprintf (msg, 75, "1");
      client.publish("home/smoke/smoke" , msg);
      Serial.println(" smk");
        }
        
    if(digitalRead(pir)==HIGH && (now - lastMsgpir > 10000))  {
    // Publish
      lastMsgpir = now;
      snprintf (msg, 75, "1");
      client.publish("home/pir/smoke" , msg);
      Serial.println(" pir");
        }
}
