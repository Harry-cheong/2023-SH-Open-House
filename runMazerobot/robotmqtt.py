import paho.mqtt.client as mqtt
import time
import sys
import pybricks

class Robot():
    def __init__(self):

        # Robot Status
        self.status = "Free"
        
        # Robot Motors



        # Robot Sensors 



        # Constants
        self.speed = 30
        
        # MQTT Client Instance
        self.client_ev3 = None

    # Adding MQTT client instance
    def addMQTT_object(self, ev3_client):
        self.client_ev3 = ev3_client

    # Commands
    def process_cmd(self, msg):
        if self.status == "Free":
            pass

    def publish_status(self):
        assert self.client is not None
        client_ev3.publish(self.status)

    # Basic Movements
    def r(self, deg):
        pass
    def l(self, deg):
        pass
    def f(self, deg):
        pass
    def b(self, deg):
        pass
    
    # Gyro
    def gf(self, deg):
        pass
    def gt(self, bearing):
        pass

class client_ev3():

    # MQTT Server Info
    broker = "58.182.191.109" # Public IP4 Address 
    port = 1883

    # MQTT Auth
    username = 'algorithm'
    password = '12345'

    # Client info
    client_id = "Maze-Robot"

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
    def on_message(self, client, userdata, msg):
        self.cmd.process_cmd(msg)

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
        result = self.client.publish(self.topic, message)
        # result: [0, 1]
        # status = result[0]
        # if status == 0: print("Send {message} to topic {topic}".format(message = message, topic = self.topic))
        # else: print("Failed to send message to topic {topic}".format(topic = self.topic))



# Instances 
cmd = Robot()
ev3 = client_ev3(cmd)
cmd.addMQTT_object(ev3)

# Loop
ev3.client.loop_forever()
