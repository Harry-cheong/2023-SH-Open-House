import os
from subprocess import Popen, PIPE, TimeoutExpired
import socket
from collections import deque 
import time
import paho.mqtt 
import urllib.request

class mqtt: 
    def __init__(self, path):
        self.path = path
        self.active = False
        self.connected_to = []
    
    def getIP(self):
        self.hostname = socket.gethostname()   
        self.localIP4 = socket.gethostbyname(self.hostname) 
        self.externalIP4 = urllib.request.urlopen("https://v4.ident.me/").read().decode('utf8')
    
    def start(self):
        self.getIP()
        if not self.active:
            self.active = True
            os.chdir(self.path)
            self._server = Popen(["mosquitto", "-v", "-c", "C:\\Users\\harry\\Desktop\\SH Robotics\\2023-SH-Open-House\\MQTT Server\\mosquitto.conf"],
                            stdout = PIPE,
                            # stdin = PIPE,
                            text = True,
                            universal_newlines = True,
                            # capture_output = True
                            )
        else:
            print("Server running...")
        

    def read(self):
        if not self.active:
            print("Server Inactive. Start Server")
            return

        try:
            print(self._server.communicate(timeout = 5))
        except TimeoutExpired:
            print("No output")

    def clients(self):
        pass
            

    def stop(self):
        if self.active:
            self._server.terminate()

class config:
    def __init__(self):
        self.getIP()
        self.port()

    def getIP(self):
        self.hostname = socket.gethostname()   
        self.localIP4 = socket.gethostbyname(self.hostname) 
        self.externalIP4 = urllib.request.urlopen("https://v4.ident.me/").read().decode('utf8')

# Config file 
s = mqtt("C:\Program Files\mosquitto")
response = ""

# Maze Runner Command info
info  = " | MQTT Server | \n server-start : starts mqtt server \n server-read : receives and outputs mqtt server thread \n server-info : outputs server info i.e. ip4 adress, hostname etc. \n server-terminate : ends mqtt server"

# Command Line
while True:
    if response:
        response = input("\n< MQTT-server >: ")
    else: 
        response = input("< MQTT-server >: ")
    
    # MQTT Server
    if response == "help":
        print(info)
    
    elif response == "server-start":
        s.start()
    elif response == "server-terminate":
        s.stop()
        break
    elif response == "server-read":
        s.read()

    elif response == "server-info":
        if s.active:
            print(f"server-hostname = {s.hostname}")
            print(f"server-localip4 = {s.localIP4}")
            print(f"server-externalip4 = {s.externalIP4}")
        else:
            print("Server Inactive. Start Server")

    else:
        print(f"MQTT-Server has no such command \"{response}\". use \"help\" for more info")
    
    time.sleep(1)




