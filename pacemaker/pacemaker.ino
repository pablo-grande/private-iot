
#include "PubSubClient.h" // Connect and publish to the MQTT broker

// Code for the ESP32
#include "WiFi.h" // Enables the ESP32 to connect to the local network (via WiFi)


// Code for the ESP8266
//#include "ESP8266WiFi.h"  // Enables the ESP8266 to connect to the local network (via WiFi)
//#define DHTPIN D5         // Pin connected to the DHT sensor


// WiFi
// TODO: Add in secrets.h
const char* ssid = "MIWIFI_5G_6deK";                 // Your personal network SSID
const char* wifi_password = "gJxx6kGY"; // Your personal network password

// MQTT
// TODO: Add in secrets.h
const char* mqtt_server = "192.168.1.240";  // IP of the MQTT broker
const char* tension = "patient/tension/mmHg";
const char* beats = "patient/beats/bpm";
// TODO: Implement if time left
//const char* mqtt_username = "iot"; // MQTT username
//const char* mqtt_password = "iot"; // MQTT password
const char* clientID = "pacemaker"; // MQTT client ID

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
// 1883 is the listener port for the Broker
PubSubClient client(mqtt_server, 1883, wifiClient); 


void connect_WiFi() {
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect to the WiFi
  WiFi.begin(ssid, wifi_password);

  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Debugging - Output the IP Address of the ESP8266
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void connect_MQTT(){
  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  // If the connection is failing, make sure you are using the correct MQTT Username and Password (Setup Earlier in the Instructable)
  if (client.connect(clientID)) {
    Serial.println("Connected to MQTT Broker!");
  } else {
    Serial.println("Connection to MQTT Broker failed...");
  }
}

void setup() {
  Serial.begin(9600);
  connect_WiFi();
}

void loop() {
  connect_MQTT();
  Serial.setTimeout(2000);
  
  //TODO: Add some variability
  float t = 120.0;
  float bpm = 70.0;
  
  Serial.print("Tension: ");
  Serial.print(t);
  Serial.println(" mmHg");
  Serial.print("Beats: ");
  Serial.print(bpm);
  Serial.println(" bpm");

  // MQTT can only transmit strings
  String a="Tension: "+String((float)t)+" mmHg ";
  String b="Beats: "+String((float)bpm)+" bpm ";

  // PUBLISH to the MQTT Broker (topic = Temperature, defined at the beginning)
  if (client.publish(tension, String(a).c_str())) {
    Serial.println("tension sent!");
  } else {
  // Again, client.publish will return a boolean value depending on whether it succeded or not.
  // If the message failed to send, we will try again, as the connection may have broken.
    Serial.println("failed to send. Reconnecting to MQTT Broker and trying again");
    client.connect(clientID);
    delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
    client.publish(tension, String(a).c_str());
  }

  // PUBLISH to the MQTT Broker (topic = Humidity, defined at the beginning)
  if (client.publish(beats, String(b).c_str())) {
    Serial.println("beats sent!");
  } else {
  // Again, client.publish will return a boolean value depending on whether it succeded or not.
  // If the message failed to send, we will try again, as the connection may have broken.
  
    Serial.println("failed to send. Reconnecting to MQTT Broker and trying again");
    client.connect(clientID);
    delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
    client.publish(beats, String(b).c_str());
  }
  //client.disconnect();  // disconnect from the MQTT broker
  delay(1000*10);       // print new values every 10 seconds
}
