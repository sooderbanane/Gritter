import csv
import os
import paho.mqtt as mqtt
from datetime import datetime


MQTT_BROKER = "localhost"
MQTT_PORT = "1883"
MQTT_TOPIC = ["switch_1","door_1","door_2","temp_1"]

def topic_filename(topic):
    return topic.replace("/", "_") + ".csv" 

def 
