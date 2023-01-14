import paho.mqtt.client as mqtt
import sys
from buildprogram import Builder
from runpybricks import autopybricks
import threading
import logging
class Robot():
    def __init__(self):
