#!/usr/bin/python3
# coding=utf-8
import argparse
import socket
import time
from random import randint

MQTT_PORT=1883

# Dependencia: paho-mqtt==0.4.94
# Si bien esa versión es vieja, es la que funciona con mosquitto version 0.15 que es el posible instalarle a la máquina virtual Cooja
# pip install paho-mqtt==0.4.94

try:
  import paho.mqtt.client as mqtt
except:
  print ("Imposible to connect with broker.")
  print ("Intente con: pip3 install")
  exit(1)

# Parseo de arguments
parser = argparse.ArgumentParser()
parser.add_argument("host", help="Una ipv4.")
parser.add_argument("topic", help="Un topico. Por ejemplo test/hello")
parser.add_argument("-i", "--interval", help="interval in seconds to repeat query. 60 segs by default", type=int, action="store")
parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
args = parser.parse_args()

broker= args.host
topic= str(args.topic)
client = mqtt.Client("mqtt")


try:
    client.connect(broker) 
except:
    print ("Error to conect to broker")
    exit(1)

while True:
    try:  
      
        value = randint(0,100)
        print "Se envía " + str(value) + " al topico " + str(topic)
        print "---------------------------------------"
        client.publish(topic, str(value))
        if args.interval:
            time.sleep(int(args.interval))
        else:
            time.sleep(60)
    except KeyboardInterrupt:
      print('Interrupted by keyboard!')
      break

