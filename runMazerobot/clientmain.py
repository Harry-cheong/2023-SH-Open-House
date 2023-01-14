import paho.mqtt.client as mqtt
import sys
from buildprogram import Builder
from runpybricks import autopybricks
import threading
import logging
class Robot():
    def __init__(self):

        # Robot Status
        self.status = "Free"
        self.status_published = False
        
        # MQTT Client Instance
        self.client_ev3 = None

        # Builder
        self.fileb = Builder()

        # Pybricks
        self.pyb = autopybricks()
        self.pyb_isprogramrunning = False
        
        # Threading
        self.cmd_processor1 = threading.Thread()
        self.cmd_processor2 = threading.Thread()

    # Adding MQTT client instance
    def addMQTT_object(self, ev3_client):
        self.client_ev3 = ev3_client

    # Commands
    #TODO test whether threading works
    def _process_cmd(self, client, msg):
        if not self.cmd_processor1.is_alive():
            self._cmdprocessor1 = threading.Thread(target = self.process_cmd, args=(client, msg,))
            self._cmdprocessor1.start()
        elif not self.cmd_processor2.is_alive():
            self._cmdprocess2 = threading.Thread(target = self.process_cmd, args=(client, msg,))
            self._comdprocessor.start()
        else:
            self.client_ev3.publish("Client Overloaded. Too many command requests")
        
    def process_cmd(self, client, msg):
        # print(client)

        if client != self.client_ev3.client_id: # making sure that the msg received is not from the client itself

            if self.status == "Free": 

                # Responding to run cmd
                if msg[:3] == "Run":
                    self.status = "Running"

                    # Publishes status to guis
                    self.client_ev3.publish("Received")

                    # Building cmd.txt
                    robotcmd = msg[msg.find("[") : ]
                    self.fileb.buildcmds(robotcmd)

                    # Copies cmd.txt and runs it on pybricks
                    self.pyb.runcmd()

                    # Checking for when the robot is done executing the program
                    self.pyb_isprogramrunning = True
                    self.pyb.load(timeout = 0.5)
                    while self.pyb.Isprogramrunning():
                        pass
                    self.pyb_isprogramrunning = False
                    self.pyb.exit()
                    
                    self.status = "Free"
                    self.status_published = False
                    self.publish_status()
                    # print("status received")
            
            elif msg == "Interrupt execution":
                self.pyb.stopprogram()


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
    
    # The callback for when the client receives the published message
    def on_publish(self, client, userdata, mid):
        print("Successful")

    # The callback for when the client receives a CONNACK response from the server
    def on_connect(self, client, userdata, flags, rc):
        logging.info(f"[Local] Connected to broker@{self.broker}.{self.port}")
        if int(rc) == 0 : print("Connected")
        else: print("Connection Failed.")
    
    # The callback for when a PUBLIC message message is received from the server
    def on_message(self, _client, userdata, msg):
        decrypted_data = str(msg.payload.decode("utf-8"))
        logging.info(decrypted_data)
        print(decrypted_data)

        msg_filtered = decrypted_data[decrypted_data.find("]") + 2 :]
        client = decrypted_data[: decrypted_data.find("]") + 1].replace("[", "").replace("]","")

        self.cmd._process_cmd(client, msg_filtered)

    # Function to connect with server
    def connect_mqtt(self):

        client = mqtt.Client(self.client_id)

        # Authentication 
        client.username_pw_set(self.username, self.password)

        # Callbacks
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_publish = self.on_publish
        
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
    
if __name__ == "__main__":

    # Logging 
    file_handler = logging.FileHandler(filename=r"C:\Users\harry\Desktop\SH Robotics\2023-SH-Open-House\runMazerobot\logs.txt",mode="a")
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(format='%(asctime)s - %(message)s',level=logging.INFO, handlers=handlers)

    # Instances 
    cmd = Robot()
    ev3 = client_ev3(cmd)
    cmd.addMQTT_object(ev3)

    # Start Loop
    cmd.start()

    # Loop
    ev3.client.loop_forever()

    # End Log 
    logging.info("[Local] Session Ended \n\n")
