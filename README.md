# LightSwarm
A Swarm Intelligence project involving interacting Esp8266 nodes and a master Raspberry pi acting as the hub. Integration with IBM cloud bluemix has also been done through nodered where the message broadcast (Light sensor value) as UDP from the Master ESP8266 to the Raspberry pi is being stored on the cloudant DB. Integration with cloudant DB has also been done where all the values from the DB are fetched and their avg is computed.

In this project, I used Node-RED to connect Raspberry Pi to IBM Bluemix. This project uses the light data collected from the ESP Swarm, and sends them to Raspberry Pi. The data are then sent from Raspberry Pi to Bluemix, and saved on a database. Once they are in the Bluemix database, I used cloudant integration code to access it anytime from anywhere for computing average purpose. I also used Node-RED to send mail to my gmail with the light reading that crosses the threshold value.

