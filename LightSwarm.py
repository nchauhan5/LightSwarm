'''
    LightSwarm Raspberry Pi Logger
    SwitchDoc Labs
'''

import sys
import time
import random

from netifaces import interfaces, ifaddresses, AF_INET

from socket import *

# Import the TCS34725 module.
import Adafruit_TCS34725

# Import Adafruit GPIO library
import RPi.GPIO as GPIO

VERSIONNUMBER = 6
# packet type definitions
LIGHT_UPDATE_PACKET = 0
RESET_SWARM_PACKET = 1
CHANGE_TEST_PACKET = 2   # Not Implemented
RESET_ME_PACKET = 3
DEFINE_SERVER_LOGGER_PACKET = 4
LOG_TO_SERVER_PACKET = 5
MASTER_CHANGE_PACKET = 6
BLINK_BRIGHT_LED = 7

MYPORT = 2916
MYPORT_OUT = 2927
SWARMSIZE = 5

logString = ""

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(11, GPIO.OUT)

# Create a TCS34725 instance with default integration time (2.4ms) and gain (4x).
tcs = Adafruit_TCS34725.TCS34725 (integration_time = Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_700MS, gain = Adafruit_TCS34725.TCS34725_GAIN_1X)

# Disable interrupts (can enable them by passing true, see the set_interrupt_limits function too).
tcs.set_interrupt(True)

# UDP Commands and packets

def SendDEFINE_SERVER_LOGGER_PACKET(s):
        print "DEFINE_SERVER_LOGGER_PACKET Sent"
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # get IP address
        for ifaceName in interfaces():
                addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
                print '%s: %s' % (ifaceName, ', '.join(addresses))

        # last interface (wlan0) grabbed
        print addresses
        myIP = addresses[0].split('.')
        print myIP
        data= ["" for i in range(14)]

        data[0] = chr(0xF0)
        data[1] = chr(DEFINE_SERVER_LOGGER_PACKET)
        data[2] = chr(0xFF) # swarm id (FF means not part of swarm)
        data[3] = chr(VERSIONNUMBER)
        data[4] = chr(int(myIP[0])) # first octet of ip
        data[5] = chr(int(myIP[1])) # second octet of ip
        data[6] = chr(int(myIP[2])) # third octet of ip
        data[7] = chr(int(myIP[3])) # fourth octet of ip
        data[8] = chr(0x00)
        data[9] = chr(0x00)
        data[10] = chr(0x00)
        data[11] = chr(0x00)
        data[12] = chr(0x00)
        data[13] = chr(0x0F)

        s.sendto(''.join(data), ('<broadcast>', MYPORT))

def SendRESET_SWARM_PACKET(s):
        print "RESET_SWARM_PACKET Sent"
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        data= ["" for i in range(14)]

        data[0] = chr(0xF0)
        data[1] = chr(RESET_SWARM_PACKET)
        data[2] = chr(0xFF)
        data[3] = chr(VERSIONNUMBER)
        data[4] = chr(0x00)
        data[5] = chr(0x00)
        data[6] = chr(0x00)
        data[7] = chr(0x00)
        data[8] = chr(0x00)
        data[9] = chr(0x00)
        data[10] = chr(0x00)
        data[11] = chr(0x00)
        data[12] = chr(0x00)
        data[13] = chr(0x0F)

        s.sendto(''.join(data), ('<broadcast>', MYPORT))


def parseLogPacket(message):

        incomingSwarmID = setAndReturnSwarmID(ord(message[2]))
        print "Log From SwarmID:",ord(message[2])
        print "Swarm Software Version:", ord(message[4])

        print "StringLength:",ord(message[3])
        logString = ""
        for i in range(0,ord(message[3])):
                logString = logString + chr(ord(message[i+5]))

        print "logString:", logString
        return logString


def setAndReturnSwarmID(incomingID):


        for i in range(0,SWARMSIZE):
                if (swarmStatus[i][5] == incomingID):
                        return i
                else:
                        if (swarmStatus[i][5] == 0):  # not in the system, so put it in

                                swarmStatus[i][5] = incomingID;
                                print "incomingID %d " % incomingID
                                print "assigned #%d" % i
                                return i


        # if we get here, then we have a new swarm member.
        # Delete the oldest swarm member and add the new one in
        # (this will probably be the one that dropped out)

        oldTime = time.time();
        oldSwarmID = 0
        for i in range(0,SWARMSIZE):
                if (oldTime > swarmStatus[i][1]):
                        oldTime = swarmStatus[i][1]
                        oldSwarmID = i




        # remove the old one and put this one in....
        swarmStatus[oldSwarmID][5] = incomingID;
        # the rest will be filled in by Light Packet Receive
        print "oldSwarmID %i" % oldSwarmID

        return oldSwarmID


# set up sockets for UDP

s=socket(AF_INET, SOCK_DGRAM)
host = 'localhost';
s.bind(('',MYPORT))

sock = socket(AF_INET, SOCK_DGRAM) # Internet

print "--------------"
print "LightSwarm Logger"
print "Version ", VERSIONNUMBER
print "--------------"


# first send out DEFINE_SERVER_LOGGER_PACKET to tell swarm where to send logging information

SendDEFINE_SERVER_LOGGER_PACKET(s)
time.sleep(3)
#SendDEFINE_SERVER_LOGGER_PACKET(s)

# swarmStatus
swarmStatus = [[0 for x  in range(6)] for x in range(SWARMSIZE)]

# 6 items per swarm item

# 0 - NP  Not present, P = present, TO = time out
# 1 - timestamp of last LIGHT_UPDATE_PACKET received
# 2 - Master or slave status   M S
# 3 - Current Test Item - 0 - CC 1 - Lux 2 - Red 3 - Green  4 - Blue
# 4 - Current Test Direction  0 >=   1 <=
# 5 - IP Address of Swarm


for i in range(0,SWARMSIZE):
        swarmStatus[i][0] = "NP"
        swarmStatus[i][5] = 0

# completeCommand() # ie RasPiConnect System



while(1) :

        # receive datclient (data, addr)
        print("xyz")
        d = s.recvfrom(1024)
        message = d[0]
        addr = d[1]
        print("abc")

        #readingFromMaster = ord(message[5])*256 + ord(message[6])
        #print "********** Reading from Master readingFromMaster:",readingFromMaster
        #print ord(message[1])

        
        
        if (ord(message[1]) == LOG_TO_SERVER_PACKET):
                print "Swarm LOG_TO_SERVER_PACKET Received"

                # Read the R, G, B, C color data.
                r, g, b, c = tcs.get_raw_data()

                # Calculate lux with another utility function.
                lux = Adafruit_TCS34725.calculate_lux(r, g, b)
                print "Lux is ",lux

                readingFromMaster = ord(message[5])*256 + ord(message[6])
                print "********** Reading from Master readingFromMaster:",readingFromMaster
                diff = lux - readingFromMaster
                print "Diff is ",diff

                sock.sendto(str(readingFromMaster), ("127.0.0.1", MYPORT_OUT))

                if(diff > 800 or diff < -800):
                        SendRESET_SWARM_PACKET(s)
                        GPIO.output(11, GPIO.HIGH)
                        time.sleep(1);
                        GPIO.output(11, GPIO.LOW)

                else:
                        print "Difference not enough to reset the swarm"
