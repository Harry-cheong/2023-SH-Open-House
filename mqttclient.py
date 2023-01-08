#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import sys

class client_ev3():
    broker = '58.182.191.109' # Public IP4 Address 
    port = 1883
    # topic = 'rubrikcube/cubeface' 
    # topic = 'rubrikcube/solution'

    client_id = 'Rubrik Cube Solver'
    username = 'algorithm'
    password = '12345'
    timeout_reconnect = 120

    def __init__(self):
        self.topic = 'rubrikcube/cubeface'
        self.ev3_present = False
        self.messages = []

        self.client = self.connect_mqtt()
    
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt.Client(self.client_id)
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def checkforcomp(self):
        self.client.subscribe(self.topic)
        #  self.publish(self.client, 'ev3')
        self.client.on_message = self.on_message
        print(self.messages)
        self.client.loop_forever

    def publish(self, client, message):
        msg_count = 0
        time.sleep(1)
        result = client.publish(self.topic, message)
        # result: [0, 1]
        status = result[0]
        # if status == 0: print("Send {message} to topic {topic}".format(message = message, topic = self.topic))
        # else: print("Failed to send message to topic {topic}".format(topic = self.topic))

    # The callback for when a PUBLISH message is received from the server.
    def swap_channel(self):
        pass

    def on_message(self,client, userdata, msg):
        self.messages.append(msg.payload) 

print('hello')
ev3 = client_ev3()
ev3.checkforcomp()