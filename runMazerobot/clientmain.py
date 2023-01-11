import paho.mqtt.client as mqtt
import time
import sys
import pybricks
from buildprogram import Builder
from runpybricks import autopybricks

class Robot():
    def __init__(self):

        # Robot Status
        self.status = "Free"
        self.status_published = False
        
        # MQTT Client Instance
        self.client_ev3 = None

        # Builder
        self.fileb = Builder()

    # Adding MQTT client instance
    def addMQTT_object(self, ev3_client):
        self.client_ev3 = ev3_client

    # Commands
    def process_cmd(self, client, msg):
        # print(client)
        if client != self.client_ev3.client_id:
            if self.status == "Free":
                self.status = "Running"

                #TODO Execute commands in msg
                self.client_ev3.publish("Command Received. Running...")

                # Simulation of robot execution
                time.sleep(5)
                #TODO Incorporation of builder + autopybricks

                self.status = "Free"
                self.status_published = False
                self.publish_status()

            elif self.status == "Running": 
                print("Program Running in Progress...")

    def publish_status(self):
        if not self.status_published:
            self.client_ev3.publish("Status: " + self.status)
            self.status_published = True

    # start
    def start(self):
        self.publish_status()

class client_ev3():

    # MQTT Server Info
    broker = "58.182.191.109" # Public IP4 Address 
    # broker = "172.30.192.1"
    port = 1883

    # MQTT Auth
    username = 'algorithm'
    password = '12345'

    # Client info
    client_id = "Mazerunner"

    # MQTT Channel
    topic = "Comms" 

    def __init__(self, cmd):
        self.messages = []
        
        self.cmd = cmd
        # MQTT Client Instance
        self.client = self.connect_mqtt()
    
    # The callback for when the client receives a CONNACK response from the server
    def on_connect(self, client, userdata, flags, rc):
        if int(rc) == 0 : print("Connected")
        else: print("Connection Failed.")
    
    # The callback for when a PUBLIC message message is received from the server
    def on_message(self, _client, userdata, msg):
        decrypted_data = str(msg.payload.decode("utf-8"))


        client = decrypted_data[: decrypted_data.find("]") + 1].replace("[", "").replace("]","")

        print(decrypted_data)
        self.cmd.process_cmd(client, decrypted_data)

    # Function to connect with server
    def connect_mqtt(self):

        client = mqtt.Client(self.client_id)

        # Authentication 
        client.username_pw_set(self.username, self.password)

        # Callbacks
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        
        # Connect
        client.connect(self.broker, self.port)

        # Subscribe
        client.subscribe(self.topic)

        return client


    def publish(self, message):
        result = self.client.publish(self.topic, f"[{self.client_id}] " + message)
        # result: [0, 1]
        status = result[0]
        if not status == 0: print(f"Failed to send {message} to topic {self.topic}")



# Instances 
cmd = Robot()
ev3 = client_ev3(cmd)
cmd.addMQTT_object(ev3)

# Start Loop
cmd.start()

# Loop
ev3.client.loop_forever()
