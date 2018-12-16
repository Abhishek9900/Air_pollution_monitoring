#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);
int count = 0;
void setup() {
  
Serial.begin(115200);
WiFi.begin("Kripal_access_point_name", "password_here");  //Connect to the WiFi network

while (WiFi.status() != WL_CONNECTED) {  //Wait for connection

delay(500);
Serial.println("Waiting to connect…");

}

Serial.print("IP address: ");
Serial.println(WiFi.localIP());                         //Print the local IP of the webserver

server.on("/Python", handlePath);              //Associate the handler function to the path
server.begin();                                                   //Start the server
Serial.println("Server listening");
}

void loop() {
server.handleClient(); //Handling of incoming requests
}

void handlePath() { //Handler for the path

server.send(200, "text/plain", String(count));
Serial.println(count);
count += 1;
delay(5000);
}
