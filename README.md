# LightSwarm
A Swarm Intelligence project involving interacting Esp8266 nodes and a master Raspberry pi acting as the hub

In this project, I used Node-RED to connect Raspberry Pi to IBM Bluemix. This project uses the light data collected from the ESP Swarm, and sends them to Raspberry Pi. The data are then sent from Raspberry Pi to Bluemix, and saved on a database. Once they are in the Bluemix database, I used cloudant integration code to access it anytime from anywhere for computing average purpose. I also used Node-RED to send mail to my gmail with the light reading that crosses the threshold value.
